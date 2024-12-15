import time
import json
import requests
from flask import request, jsonify, render_template, session, redirect

from loguru import logger
from .modeling.inference import InferencePipeline


def setup_routes(app):
    @app.route('/')
    def home():
        '''
        Renders application homescreen page with a user form.
        '''
        logger.info("Accessed root page")
        return render_template('index.html')


    @app.route('/itinerary/generate', methods=['POST'])
    def generate_itinerary_route():
        '''
        API starts the inference pipeline based on the user input and returns the itinerary data.
        '''
        user_input = request.json
        logger.info(f"Received user input: {user_input}")

        if app.config['DEBUG']: # To save time and credits uploads premade itinerary in case of debugging
            logger.info('>>>>> Inference started <<<<<')
            with open('triptailor/modeling/itinerary_example.json', 'r') as file:
                itinerary_json = json.load(file)
            time.sleep(1) # Imitate delay
            logger.info('>>>>> Inference completed <<<<<')
        else:
            logger.info('>>>>> Inference started <<<<<')
            _, _, itinerary_json = InferencePipeline().run_inference(user_input)
            logger.info('>>>>> Inference completed <<<<<')
        
        session['itinerary'] = itinerary_json
        return jsonify(itinerary_json), 200


    @app.route('/itinerary')
    def itinerary():
        '''
        Renders page with the itinerary information.
        '''
        logger.info("Accessed itinerary page")
        itinerary_data = session.get('itinerary', {})
        if not app.config['DEBUG']:
            if not itinerary_data:
                return redirect('/')
            try:
                itinerary_data = json.loads(itinerary_data)
            except json.JSONDecodeError:
                logger.error("Error: itinerary_data is not valid JSON.")
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
        '''
        API to add images to pdf mitigating browser's limitations.
        '''
        image_url = request.args.get('url')
        response = requests.get(image_url, stream=True)
        headers = {
            "Content-Type": response.headers["Content-Type"]
        }
        return response.content, response.status_code, headers
    
    
    @app.route('/config/')
    def config():
        '''
        Shows configuration data
        '''
        s = []
        s.append('debug: '+str(app.config['DEBUG']))
        s.append('port: '+str(app.config['port']))
        s.append('url: '+app.config['url'])
        s.append('ip_address: '+app.config['ip_address'])
        return ', '.join(s)
