# TODO
# Itinerary is stored in a global dict



from flask import Flask, request, jsonify, render_template, session, redirect
import json
import secrets
from modeling.inference import InferencePipeline
from loguru import logger
from dotenv import load_dotenv

_ = load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
itinerary_store = {}

@app.route('/itinerary/generate', methods=['POST'])
def generate_itinerary_route():
    """
    Endpoint to generate a travel itinerary based on user input.
    """
    #try:
    # Parse input JSON
    user_input = request.json ### EMPTY INPUT NOW
    print("USER INPUT", user_input)
    logger.info("Received user input: %s", user_input)
    
    # Validate required fields
    #required_fields = ['budget', 'duration', 'destination']
    #missing_fields = [field for field in required_fields if field not in user_input]
    #if missing_fields:
    #    return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    
    with open('triptailor/modeling/itinerary_example.json', 'r') as file:
        itinerary_json = json.load(file)
    
    
    #user_prompt = """
    #    I am planning a 3-day family trip to Italy. We enjoy historical sites, good food, and outdoor activities. \
    #    We’d like to visit different cities and explore famous landmarks, but also have some relaxing days in nature. \
    #    Would like to keep one day without any activities, just to stay at the hotel and rest.\
    #    Our budget is moderate, and we prefer shorter travel distances between destinations.
    #    """

    #logger.info('>>>>> Inference started <<<<<')
    #_, _, itinerary_json = InferencePipeline().run_inference(user_prompt)
    #logger.info('>>>>> Inference completed <<<<<')
    
    itinerary_store['itinerary'] = itinerary_json

    return jsonify(itinerary_json), 200
    #except Exception as e:
    #    logger.error("Error generating itinerary: %s", e)
    #    return jsonify({'error': 'Internal server error'}), 500


@app.route('/')
def home():
    """
    Basic route to confirm the server is running.
    """
    return render_template('index.html')


@app.route('/itinerary')
def itinerary():

    itinerary_data = itinerary_store['itinerary']

    if not itinerary_data:
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


if __name__ == '__main__':
    # Set the debug mode to True for development purposes
    app.run(host='0.0.0.0', port=5000, debug=True)
