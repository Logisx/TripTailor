from dotenv import load_dotenv

_ = load_dotenv()

from langgraph.graph import StateGraph, END

from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage, ToolMessage

from modeling.prompts import PREFERENCES_EXTRACTION_PROMPT, IDEAS_GENERATION_PROMPT, ITINERARY_PLANNING_PROMPT
from modeling.data_schemas import user_preferences_parser, travel_ideas_parser, itinerary_parser, AgentState
from modeling.tools.google_maps_tool import GoogleMapsTool
from loguru import logger

class Agent:
    def __init__(self, model, checkpointer, tools=None, system=""):
        logger.info("Agent initialization started")
        self.system = system
        builder = StateGraph(AgentState)
        builder.add_node("preferences_extraction", self._preferences_extraction_node)
        builder.add_node("ideas_generation", self._ideas_generation_node)
        builder.add_node("itinerary_planning", self._itinerary_planning_node)
        builder.add_node("adding_maps_info", self._add_geolocation_and_image_node)
        builder.set_entry_point("preferences_extraction")
        builder.add_edge("preferences_extraction", "ideas_generation")
        builder.add_edge("ideas_generation", "itinerary_planning")
        builder.add_edge("itinerary_planning", "adding_maps_info")
        self.graph = builder.compile(checkpointer=checkpointer)
        if tools:
            self.tools = {t.name: t for t in tools}
            self.model = model.bind_tools(tools)  
        else:
            self.model = model  
        logger.info("Agent initialized")


    def _preferences_extraction_node(self, state: AgentState):
        logger.info("Calling preferences extraction node")
        chain = PREFERENCES_EXTRACTION_PROMPT | self.model | user_preferences_parser
        response = chain.invoke({"user_query": state['user_query']})
        return {"user_preferences": response}


    def _ideas_generation_node(self, state: AgentState):
        logger.info("Calling ideas generation node")
        chain = IDEAS_GENERATION_PROMPT | self.model | travel_ideas_parser
        response = chain.invoke({"user_preferences": state['user_preferences']})
        return {"travel_ideas": response}


    def _itinerary_planning_node(self, state: AgentState):
        logger.info("Calling itinerary planning node")
        chain = ITINERARY_PLANNING_PROMPT | self.model | itinerary_parser
        response = chain.invoke({"user_preferences": state['user_preferences'], "travel_ideas": state['travel_ideas']})
        return {"itinerary": response}


    def _add_geolocation_and_image_node(self, state: AgentState):
        logger.info("Calling google maps tool node")
        google_maps_tool = GoogleMapsTool()
        itinerary = state['itinerary']
        enhanced_itinerary = []

        # Iterate over each day in the itinerary
        for day in itinerary['daily_itineraries']:
            enhanced_activities = []
            
            # Iterate over each major activity for the day
            for activity in day['activities']:
                # Enhance main activity destinations
                enhanced_main_activity = []
                for destination in activity['main_activity']:
                    # Call the Google Maps Tool to get geolocation and image
                    response = google_maps_tool.invoke({"destination": destination['name']})
                    
                    # Add the enhanced data (geolocation and image URL) to the destination
                    destination['geolocation'] = response.get('geolocation')
                    destination['image_url'] = response.get('image_url')
                    
                    # Add the enhanced destination to the main activity list
                    enhanced_main_activity.append(destination)

                # Add the enhanced activity (without alternatives)
                enhanced_activity = {
                    "main_activity": enhanced_main_activity
                }
                enhanced_activities.append(enhanced_activity)

            # Update the day's activities with the enhanced activities
            day['activities'] = enhanced_activities
            enhanced_itinerary.append(day)

        # Return the enhanced itinerary
        return {"itinerary": {"daily_itineraries": enhanced_itinerary}}

