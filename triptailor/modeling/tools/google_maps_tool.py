import requests
import os

class GoogleMapsTool:
    BASE_URL = "https://maps.googleapis.com/maps/api/place"

    def __init__(self):
        # Load the API key from the .env file
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key not found in .env file. Please ensure GOOGLE_API_KEY is set.")


    def place_search(self, query):
        """Search for a place using the text search method."""
        search_url = f"{self.BASE_URL}/textsearch/json"
        params = {
            "query": query,
            "key": self.api_key
        }
        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0]  # Return the first result
        return None

    def place_details(self, place_id):
        """Retrieve detailed information about a place using its place_id."""
        details_url = f"{self.BASE_URL}/details/json"
        params = {
            "place_id": place_id,
            "key": self.api_key,
            "fields": "name,geometry,photo"  # Specify the fields you want in the response
        }
        response = requests.get(details_url, params=params)
        if response.status_code == 200:
            return response.json().get("result", {})
        return None

    def get_image_url(self, photo_reference, max_width=400):
        """Retrieve an image URL for a place using its photo reference."""
        if not photo_reference:
            return None
        return f"{self.BASE_URL}/photo?maxwidth={max_width}&photoreference={photo_reference}&key={self.api_key}"

    def invoke(self, args):
        """Invoke the Google Maps Tool with destination input."""
        destination_name = args.get("destination")
        
        # 1. Use Place Search to get the place_id and basic details
        place_search_result = self.place_search(destination_name)
        if not place_search_result:
            return {"error": f"Place '{destination_name}' not found."}

        place_id = place_search_result.get("place_id")
        if not place_id:
            return {"error": "Place ID not found in search results."}

        # 2. Use Place Details to get geolocation and photo reference
        place_details = self.place_details(place_id)
        if not place_details:
            return {"error": "Place details not found."}

        geolocation = place_details.get("geometry", {}).get("location")
        photo_reference = place_details.get("photos", [{}])[0].get("photo_reference")

        # 3. Generate image URL using photo reference
        image_url = self.get_image_url(photo_reference) if photo_reference else None

        # Return structured response with geolocation and image URL
        return {
            "geolocation": geolocation,
            "image_url": image_url
        }
