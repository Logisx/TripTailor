from dotenv import load_dotenv

_ = load_dotenv()

from langgraph.graph import StateGraph, END

from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage, ToolMessage

from ..modeling.prompts import PREFERENCES_EXTRACTION_PROMPT, IDEAS_GENERATION_PROMPT, ITINERARY_PLANNING_PROMPT
from ..modeling.data_schemas import user_preferences_parser, travel_ideas_parser, itinerary_parser, AgentState
from ..modeling.tools.google_maps_tool import GoogleMapsTool
from loguru import logger

class Agent:
    '''
    AI agent capable of generating personalized travel itinerary based on the user preferences
    '''
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
        user_input = state['user_input']
        response = chain.invoke({"user_query": user_input['tripDescription'],
                                  "budget": user_input['budget'],
                                  "people_number": user_input['people'],
                                  "start_date": user_input['startDate'],
                                  "end_date": user_input['endDate'],
                                  "vibe": user_input['vibe'],
                                  "interests": user_input['interests']
                                  })
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

        for day in itinerary['daily_itineraries']:
            enhanced_activities = []
            
            for activity in day['activities']:
                enhanced_main_activity = []
                for destination in activity['main_activity']:
                    response = google_maps_tool.invoke({"destination": str(itinerary['destination_country']+','+destination['name'])})
                    
                    destination['geolocation'] = response.get('geolocation')
                    destination['image_url'] = response.get('image_url')
                    
                    enhanced_main_activity.append(destination)

                enhanced_activity = {
                    "main_activity": enhanced_main_activity
                }
                enhanced_activities.append(enhanced_activity)

            day['activities'] = enhanced_activities
            enhanced_itinerary.append(day)

        return {"itinerary": {"daily_itineraries": enhanced_itinerary}}

