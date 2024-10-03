from dotenv import load_dotenv

_ = load_dotenv()

from langgraph.graph import StateGraph, END

from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage, ToolMessage

from prompts import PREFERENCES_EXTRACTION_PROMPT, IDEAS_GENERATION_PROMPT, ITINERARY_PLANNING_PROMPT
from data_schemas import user_preferences_parser, travel_ideas_parser
from data_schemas import AgentState


class Agent:
    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system
        builder = StateGraph(AgentState)
        builder.add_node("preferences_extraction", self._preferences_extraction_node)
        builder.add_node("ideas_generation", self._ideas_generation_node)
        builder.add_node("itinerary_planning", self._itinerary_planning_node)
        builder.set_entry_point("preferences_extraction")
        builder.add_edge("preferences_extraction", "ideas_generation")
        builder.add_edge("ideas_generation", "itinerary_planning")
        self.graph = builder.compile(checkpointer=checkpointer)
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)    

    def _preferences_extraction_node(self, state: AgentState):
        chain = PREFERENCES_EXTRACTION_PROMPT | self.model | user_preferences_parser
        response = chain.invoke({"user_query": state['user_query']})
        return {"user_preferences": response}


    def _ideas_generation_node(self, state: AgentState):
        chain = IDEAS_GENERATION_PROMPT | self.model | travel_ideas_parser
        response = chain.invoke({"user_preferences": state['user_preferences']})
        return {"travel_ideas": response}


    def _itinerary_planning_node(self, state: AgentState):
        messages = [
            SystemMessage(
                content=ITINERARY_PLANNING_PROMPT.format(travel_ideas=state['travel_ideas'], user_preferences=state['user_preferences'])
            )
            ]
        response = self.model.invoke(messages)
        return {"itinerary": response.content}




