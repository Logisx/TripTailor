# TODO

# Fix buttons on index





from flask import Flask, request, jsonify, render_template, session, redirect
from flask_session import Session
import json
import time
import redis
import os
import requests
import secrets
import configparser
from modeling.inference import InferencePipeline
from loguru import logger
from dotenv import load_dotenv

_ = load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def init(app):
    config = configparser.ConfigParser()
    config_location = "triptailor/etc/defaults.cfg"
    
    try:
        print("INIT FUNCTION")
        if not config.read(config_location):
            raise FileNotFoundError(f"Config file not found at: {config_location}")

        # Safely populate app.config with defaults for missing keys
        app.config['DEBUG'] = config.getboolean("config", "debug", fallback=False)
        app.config['ip_address'] = config.get("config", "ip_address", fallback="127.0.0.1")
        app.config['port'] = config.getint("config", "port", fallback=5000)
        app.config['url'] = config.get("config", "url", fallback="http://127.0.0.1:5000")
        
        # Redis configuration
        # Part of the code taken from https://testdriven.io/blog/flask-server-side-sessions/
        try:
            app.secret_key = os.getenv('FLASK_APP_SECRET_KEY', default='BAD_SECRET_KEY')

            # Configure Redis for storing the session data on the server-side
            app.config['SESSION_TYPE'] = config.get("config", "session_type", fallback='redis')
            app.config['SESSION_PERMANENT'] = False
            app.config['SESSION_USE_SIGNER'] = True
            app.config['SESSION_REDIS'] = redis.from_url(config.get("config", "redis_url", fallback="redis://127.0.0.1:6379"))
        except:
            logger.error("Redis configuration error")
    
    except Exception as e:
        print(f"Error loading configs from {config_location}: {e}")
        # Provide fallback/default values if config loading fails
        app.config['DEBUG'] = False
        app.config['ip_address'] = "127.0.0.1"
        app.config['port'] = 5000
        app.config['url'] = "http://127.0.0.1:5000"

init(app)



#itinerary_store = {}
server_session = Session(app)





@app.route('/config/')
def config():
    s = []
    s.append('debug: '+str(app.config['DEBUG']))
    s.append('port: '+app.config['port'])
    s.append('url: '+app.config['url'])
    s.append('ip_address: '+app.config['ip_address'])
    return ', '.join(s)


@app.route('/loading', methods=['GET'])
def loading_page():
    return render_template('loading.html')


@app.route('/itinerary/generate', methods=['POST'])
def generate_itinerary_route():
    """
    Endpoint to generate a travel itinerary based on user input.
    """
    user_input = request.json 
    logger.info(f"Received user input: {user_input}")

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
    if app.config['DEBUG']:
        logger.info('>>>>> Inference started <<<<<')
        with open('triptailor/modeling/itinerary_example.json', 'r') as file:
            itinerary_json = json.load(file)
        time.sleep(1) # To imitate delay
        logger.info('>>>>> Inference completed <<<<<')
    else:
        logger.info('>>>>> Inference started <<<<<')
        _, _, itinerary_json = InferencePipeline().run_inference(user_input)
        logger.info('>>>>> Inference completed <<<<<')
    
    #itinerary_store['itinerary'] = itinerary_json
    session['itinerary'] = itinerary_json
    return jsonify(itinerary_json), 200


@app.route('/')
def home():
    """
    Basic route to confirm the server is running.
    """
    return render_template('index.html')


@app.route('/itinerary')
def itinerary():

    #itinerary_data = itinerary_store['itinerary']
    itinerary_data = session['itinerary']
    print("ITINERARY DATA:", itinerary_data)

    #!!!!!!!!!!!!!!!!!!!!!!!!!
    if not app.config['DEBUG']:
        if not itinerary_data:
            return redirect('/')
        else:
            try:
                itinerary_data = json.loads(itinerary_data)
            except json.JSONDecodeError:
                print("Error: itinerary_data is not valid JSON.")
                return redirect('/')    


    trip_name = itinerary_data.get("trip_name", "Untitled Trip")
    destination_country = itinerary_data.get("destination_country", "Unknown Country")
    destination_cities = itinerary_data.get("destination_cities", "Unknown Cities")
    start_date = itinerary_data.get("start_date", "N/A")
    end_date = itinerary_data.get("end_date", "N/A")
    daily_itineraries = itinerary_data.get("daily_itineraries", [])

    return render_template(
        'itinerary.html',
        trip_name=trip_name,
        destination_country=destination_country,
        destination_cities=destination_cities,
        start_date=start_date,
        end_date=end_date,
        daily_itineraries=daily_itineraries
    )



@app.route('/proxy-image')
def proxy_image():
    image_url = request.args.get('url')
    response = requests.get(image_url, stream=True)
    headers = {
        "Content-Type": response.headers["Content-Type"]
    }
    return response.content, response.status_code, headers


if __name__ == '__main__':
    init(app)
    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port'])
    )
