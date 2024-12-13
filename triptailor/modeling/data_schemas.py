from typing import List, Optional, Dict
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage



class UserPreferences(BaseModel):
    # Basic preferences
    budget: str = Field(description="Budget range the user is able to spend (e.g., low, medium, high, extra-high)")
    trip_duration: int = Field(description="Total number of days for the trip")
    destination: str = Field(description="Primary destination or country of the trip")
    
    # Travel type and group size
    trip_type: str = Field(description="Type of trip (e.g., family trip, solo travel, couple's getaway, group travel)")
    group_size: Optional[int] = Field(description="Number of people traveling together")
    
    # Interests and activities
    interests: List[str] = Field(description="List of activities the user is interested in (e.g., museums, nature, food, nightlife, shopping)")
    
    # Preferences for locations and experiences
    accommodation_type: Optional[str] = Field(description="Preferred type of accommodation (e.g., hotel, Airbnb, hostel, resort)", default="hotel")
    preferred_travel_distance: Optional[str] = Field(description="Preferred travel distance between locations (e.g., short, medium, long)", default="medium")
    
    # Meal preferences and dietary restrictions
    meal_preferences: Optional[List[str]] = Field(description="Preferences for meals (e.g., vegetarian, vegan, local cuisine, fine dining)", default=[])
    
    # Accessibility and special requirements
    accessibility_needs: Optional[bool] = Field(description="Indicates if there are any accessibility needs (e.g., wheelchair access)", default=False)
    pet_friendly: Optional[bool] = Field(description="Indicates if pet-friendly places are preferred", default=False)
    
    # Time and season preferences
    season: Optional[str] = Field(description="Preferred season for travel (e.g., summer, winter, spring, autumn)", default="any")
    flexibility: Optional[bool] = Field(description="Indicates if the user is flexible with dates or destinations", default=True)
    
    other: Optional[List[str]] = Field(description="Any other preferences the user has", default=[])

    class Config:
        schema_extra = {
            "example": {
                "budget": "medium",
                "trip_duration": 7,
                "destination": "Italy",
                "trip_type": "family trip",
                "group_size": 4,
                "interests": ["museums", "nature", "food", "beach"],
                "accommodation_type": "resort",
                "preferred_travel_distance": "short",
                "meal_preferences": ["local cuisine", "vegetarian"],
                "accessibility_needs": False,
                "pet_friendly": False,
                "season": "summer",
                "flexibility": True,
                "other": []
            }
        }



# Define the schema for information about a city
class CityInfo(BaseModel):
    destinations: List[str] = Field(default=[], description="List of tourist destinations or attractions in the city")
    restaurants: List[str] = Field(default=[], description="List of recommended restaurants/cafes in the city")
    accomodation: List[str] = Field(default=[], description="List of suggested accomodation in the city")
    activities: Optional[List[str]] = Field(default=[], description="Popular activities or experiences to do in the city")
    events: Optional[List[str]] = Field(default=[], description="Current or upcoming events in the city")
    #shopping: Optional[List[str]] = Field(default=[], description="Recommended shopping areas or stores in the city")
    #nightlife: Optional[List[str]] = Field(default=[], description="Nightlife spots, clubs, or entertainment venues")
    #parks_nature_spots: Optional[List[str]] = Field(default=[], description="Parks, gardens, or nature spots in or near the city")
    #transportation: Optional[List[str]] = Field(default=[], description="Tips and recommendations for local transportation")
    #cultural_experiences: Optional[List[str]] = Field(default=[], description="Specific cultural experiences or activities")
    #local_tips: Optional[List[str]] = Field(default=[], description="Insider tips or local recommendations")
    #health_safety: Optional[List[str]] = Field(default=[], description="Health and safety information in the city")
    #weather_seasonal_info: Optional[List[str]] = Field(default=[], description="Average weather conditions or seasonal information")
    #day_trips: Optional[List[str]] = Field(default=[], description="Recommended day trips or nearby excursions from the city")
    #family_friendly: Optional[List[str]] = Field(default=[], description="Activities or attractions suitable for families with children")
    #pet_friendly_places: Optional[List[str]] = Field(default=[], description="Pet-friendly places such as parks, hotels, or restaurants")
    #photo_spots: Optional[List[str]] = Field(default=[], description="Suggested locations for taking memorable photos or enjoying scenic views")
    #accessibility: Optional[List[str]] = Field(default=[], description="Accessibility information for destinations, public transport, and hotels")

# Define the schema for the entire ideas generation structure
class TravelIdeas(BaseModel):
    ideas: Dict[str, CityInfo] = Field(description="Dictionary containing city names as keys and their respective information as values")
    
    class Config:
        schema_extra = {
            "example": {
                "ideas": {
                    "Rome, Italy": {
                        "destinations": ["Colosseum", "Vatican City", "Roman Forum", "Pantheon"],
                        "restaurants": ["Ristorante Aroma", "La Pergola", "Felice a Testaccio"],
                        "hotels": ["Hotel Hassler", "Hotel Eden", "The St. Regis Rome"],
                        "activities": ["Gondola ride", "Guided tour of Roman ruins", "Nighttime Colosseum tour"],
                        "shopping": ["Via Condotti", "Campo de' Fiori market"],
                        #"nightlife": ["Harry's Bar", "Live jazz at Gregory's Jazz Club"],
                        #"cultural_experiences": ["Cooking class to learn Italian cuisine"],
                        #"photo_spots": ["Gianicolo Hill", "Piazza Navona"],
                        #"parks_nature_spots": ["Villa Borghese", "Giardino degli Aranci"],
                        #"transportation": ["Best way to get around Rome is by metro", "Use public buses for sightseeing"],
                        #"local_tips": ["Avoid visiting the Colosseum on weekends", "Try local street food at Testaccio Market"],
                        #"health_safety": ["Nearest hospital: Policlinico Umberto I", "Emergency contact numbers: 112"],
                        #"weather_seasonal_info": ["Best time to visit Rome is from April to June", "Expect high temperatures in August"],
                        #"day_trips": ["Day trip to Pompeii", "Visit Tivoli for Villa d'Este"],
                        #"family_friendly": ["Visit the Children's Museum of Rome", "Explora Children's Museum"],
                        #"pet_friendly_places": ["Pet-friendly hotel: Hotel Santa Maria", "Dog park: Parco Savello"],
                        #"accessibility": ["Colosseum has an elevator for wheelchair access", "Accessible public transport routes available"],
                    },
                    "Florence, Italy": {
                        "destinations": ["Florence Cathedral", "Uffizi Gallery", "Ponte Vecchio", "Boboli Gardens"],
                        "restaurants": ["Osteria Francescana", "Enoteca Pinchiorri", "Trattoria Mario"],
                        "hotels": ["Hotel Savoy", "Four Seasons Hotel Firenze", "Villa Cora"],
                        "activities": ["Art tour of the Uffizi Gallery", "Visit to the Accademia Gallery"],
                        #"shopping": ["Via de' Tornabuoni", "Mercato Centrale"],
                        #"cultural_experiences": ["Florence Duomo climbing experience", "Cooking class in Florence"],
                        #"photo_spots": ["Piazzale Michelangelo", "View from Ponte Vecchio"],
                        #"parks_nature_spots": ["Boboli Gardens", "Giardino Bardini"]
                    }
                }
            }
        }


class Destination(BaseModel):
    name: str = Field(description="The name of the destination, e.g., 'Colosseum', 'Central Park'.")
    type: Optional[str] = Field(description="The type of the destination, e.g., 'museum', 'restaurant', 'park', etc.")
    duration: float = Field(description="Approximate time in hours to spend at this destination.")
    description: Optional[str] = Field(description="A brief description of the destination.")

class MajorActivity(BaseModel):
    main_activity: List[Destination] = Field(description="A list of destinations that represent the main activity (e.g., \
                                             walking tour including multiple places).")

class DayItinerary(BaseModel):
    date: str = Field(description="The specific date of this day in the itinerary, formatted as 'YYYY-MM-DD'.")
    activities: List[MajorActivity] = Field(description="A list of major activities planned for this day, each with a list of \
                                            destinations or sub-activities.")

class Itinerary(BaseModel):
    trip_name: Optional[str] = Field(description="Optional name or title of the trip.")
    destination_country: str = Field(description="The primary country of the trip.")
    destination_cities: str = Field(description="The primary city or cities of the trip.")
    duration: int = Field(description="Total duration of the trip in days.")
    start_date: str = Field(description="The starting date of the trip in 'YYYY-MM-DD' format.")
    end_date: str = Field(description="The ending date of the trip in 'YYYY-MM-DD' format.")
    daily_itineraries: List[DayItinerary] = Field(description="A list of daily itineraries, each representing a day of the trip.")

class Config:
    schema_extra = {
        "example": {
            "trip_name": "Family Vacation to Italy",
            "destination_country": "Italy",
            "destination_cities": "Rome, Florence, Venice",
            "duration": 5,
            "start_date": "2024-05-10",
            "end_date": "2024-05-14",
            "daily_itineraries": [
                {
                    "date": "2024-05-10",
                    "activities": [
                        {
                            "main_activity": [
                                {
                                    "name": "Colosseum",
                                    "type": "historical site",
                                    "duration": 1.5,
                                    "description": "A visit to the iconic Colosseum in Rome, Italy."
                                },
                                {
                                    "name": "Roman Forum",
                                    "type": "historical site",
                                    "duration": 1.0,
                                    "description": "Walk through the ruins of the Roman Forum, a symbol of ancient Rome."
                                },
                                {
                                    "name": "Pantheon",
                                    "type": "historical site",
                                    "duration": 1.0,
                                    "description": "Visit the ancient Roman temple, the Pantheon, now a church."
                                }
                            ]
                        },
                        {
                            "main_activity": [
                                {
                                    "name": "Lunch at Trattoria da Enzo",
                                    "type": "restaurant",
                                    "duration": 1.5,
                                    "description": "Enjoy a delicious Italian lunch at this traditional Roman restaurant."
                                }
                            ]
                        }
                    ]
                },
                {
                    "date": "2024-05-11",
                    "activities": [
                        {
                            "main_activity": [
                                {
                                    "name": "Florence Cathedral",
                                    "type": "historical site",
                                    "duration": 1.5,
                                    "description": "Explore the magnificent Florence Cathedral, also known as the Duomo."
                                },
                                {
                                    "name": "Uffizi Gallery",
                                    "type": "art museum",
                                    "duration": 2.0,
                                    "description": "Visit one of the most important art museums in Italy."
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }

class AgentState(TypedDict):
    user_query: str
    user_preferences: UserPreferences
    travel_ideas: TravelIdeas
    itinerary: str
    messages: Annotated[List[AnyMessage], operator.add]



user_preferences_parser = JsonOutputParser(pydantic_object=UserPreferences)
travel_ideas_parser = JsonOutputParser(pydantic_object=TravelIdeas)
itinerary_parser = JsonOutputParser(pydantic_object=Itinerary)
