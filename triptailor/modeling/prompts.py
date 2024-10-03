from langchain_core.prompts import PromptTemplate
from data_schemas import user_preferences_parser, travel_ideas_parser


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
    Ensure the list includes a mix of well-known and hidden gem destinations, while also considering the geographic proximity of locations to make travel between them feasible. 
    Provide more ideas than the customer can visit within the trip, as they will later decide what to include and exclude from their itinerary.
    
    Provide the travel ideas in the following structured format:
    {format_instructions}

    Customer preferences:
    {user_preferences}
    """,
    input_variables=['user_preferences'],
    partial_variables={"format_instructions": travel_ideas_parser.get_format_instructions()},
)


ITINERARY_PLANNING_PROMPT = """
    You are an expert travel agent tasked with creating a detailed trip itinerary based on the customer's preferences and a dictionary of suggested places to visit in different cities. 
    Please create an itinerary that balances key attractions and activities with the practical aspects of travel, such as distances, travel time, and meal or rest breaks. 
    Provide a structured plan, distributing activities across each day of the trip.
    For each major activity try to offer at least two alternatives so the customer may choose between them.

    Consider the following factors:
    - Prioritize activities that match the customer's preferences.
    - Ensure travel between locations is feasible, taking into account distances and available time.
    - Provide suggestions for meals or breaks at suitable times.
    - Offer a diverse range of activities to allow flexibility in planning.

    Use the search engine to look up information. \
    You are allowed to make multiple calls (either together or in sequence). \
    Only look up information when you are sure of what you want. \
    If you need to look up some information before asking a follow up question, you are allowed to do that!

    Utilize all the information below as needed:

    ------
    Customer preferences:
    {user_preferences}

    ------
    Inspiration ideas:
    {travel_ideas}
    """
