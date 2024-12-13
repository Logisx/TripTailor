from flask import Flask, request, jsonify
import logging
#from your_ai_module import generate_itinerary  # Replace with your AI pipeline module
#from google_api_utils import get_place_data  # Replace with your Google API utilities

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/itinerary/generate', methods=['POST'])
def generate_itinerary_route():
    """
    Endpoint to generate a travel itinerary based on user input.
    """
    try:
        # Parse input JSON
        user_input = request.json
        logging.info("Received user input: %s", user_input)
        
        # Validate required fields
        required_fields = ['budget', 'duration', 'destination']
        missing_fields = [field for field in required_fields if field not in user_input]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
        # Generate itinerary using AI pipeline
        itinerary = generate_itinerary(user_input)
        
        # Retrieve additional data (e.g., images, maps) using Google Places API
        for day in itinerary.get('days', []):
            for activity in day.get('activities', []):
                place_data = get_place_data(activity['location'])
                activity.update(place_data)
        
        return jsonify({'itinerary': itinerary}), 200
    except Exception as e:
        logging.error("Error generating itinerary: %s", e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/')
def home():
    """
    Basic route to confirm the server is running.
    """
    return "AI Travel Planner Backend is running!"

if __name__ == '__main__':
    # Set the debug mode to True for development purposes
    app.run(host='0.0.0.0', port=5000, debug=True)
