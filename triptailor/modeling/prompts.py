from langchain_core.prompts import PromptTemplate
from modeling.data_schemas import user_preferences_parser, travel_ideas_parser, itinerary_parser


PREFERENCES_EXTRACTION_PROMPT = PromptTemplate(
    template = """
    You are an expert travel agent tasked with extracting structured information to fill out a questionnaire about the customer's planned trip.
    Based on the customer's query, extract the key information about their trip preferences and format it accordingly.

    Provide the extracted preferences in the following structured format:
    {format_instructions}

    Customer's Query:
    {user_query}
    """,
    input_variables=["user_query"],
    partial_variables={"format_instructions": user_preferences_parser.get_format_instructions()},
)


IDEAS_GENERATION_PROMPT = PromptTemplate(
    template = """
    You are an expert travel agent tasked with creating a list of places the customer may want to visit.
    Based on the customer's preferences provided below, suggest a list of diverse places that fit the customer's interests. 
    Ensure the list includes a mix of well-known and hidden gem destinations, while also considering the geographic proximity of \
        locations to make travel between them feasible. 
    Provide more ideas than the customer can visit within the trip, as they will later decide what to include and exclude from their itinerary.
    
    Provide the travel ideas in the following structured format:
    {format_instructions}

    Customer preferences:
    {user_preferences}
    """,
    input_variables=['user_preferences'],
    partial_variables={"format_instructions": travel_ideas_parser.get_format_instructions()},
)


ITINERARY_PLANNING_PROMPT = PromptTemplate(
    template = """
    You are an expert travel agent tasked with creating a detailed trip itinerary in JSON format based on the customer's preferences and a dictionary of suggested places to visit in different cities. 
    The itinerary should be separated by days, with each day represented as a list of destinations in the order they should be visited. 
    Each destination can include any type of place, such as cafes, beaches, clubs, museums, or parks. Consider distances and travel time when creating the list of destinations for each day.

    For each day, create major activities or events that may include a list of nearby destinations grouped together (e.g., "Old Town Sightseeing" can include multiple nearby attractions).

    Each activity and destination should include an approximate time in hours that it takes to complete. Ensure meal breaks are included throughout the day, based on the time since the last meal and the user's current location.

    Provide the itinerary in the following structured format:
    {format_instructions}

    Consider the following guidelines when generating the itinerary:
    - **Group destinations logically** to form major activities or events that can include multiple destinations in close proximity.
    - **Include meal breaks** as major activities, considering the time of day and the user's proximity to recommended restaurants.
    - Take into account travel distances and time constraints when planning the order of destinations for each day.
    

    Utilize all the information below as needed:

    ------
    Customer preferences:
    {user_preferences}

    ------
    Ideas of places to visit:
    {travel_ideas}

    """,
    input_variables=["user_preferences", "travel_ideas"],
    partial_variables={"format_instructions": itinerary_parser.get_format_instructions()},
)
