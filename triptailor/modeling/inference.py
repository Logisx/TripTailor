from loguru import logger
from modeling.agent import Agent
from dotenv import load_dotenv

import json

_ = load_dotenv(override=True)

from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI

class InferencePipeline:
    '''
    Pipeline running inference from an AI agent based on the user inputted data. Returns personalized itinerary in json format.
    '''
    @staticmethod
    def run_inference(user_input=None):           
        with SqliteSaver.from_conn_string(":memory:") as memory:

            # Init the agent
            #tool = TavilySearchResults(max_results=2)
            model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            agent = Agent(model, system=user_input, checkpointer=memory)
            thread = {"configurable": {"thread_id": "1"}}
            response = []

            # Run streaming
            logger.info("Streaming the responses")
            for single_response in agent.graph.stream({'user_input': user_input}, thread):
                print(single_response)
                response.append(single_response)
            logger.info("Streaming ended")

            # Format the output to json
            response_dict = {}
            for node_response in response:
                response_dict.update(node_response)
            preferences_json = json.dumps(response_dict['preferences_extraction']['user_preferences'], indent=4)
            ideas_json = json.dumps(response_dict['ideas_generation']['travel_ideas'], indent=4)
            itinerary_json = json.dumps(response_dict['itinerary_planning']['itinerary'], indent=4)

            return preferences_json, ideas_json, itinerary_json


if __name__ == "__main__":
    try:
        logger.info('>>>>> Inference started <<<<<')

        sample_user_prompt = """
            I am planning a 3-day family trip to Italy. We enjoy historical sites, good food, and outdoor activities. \
            We’d like to visit different cities and explore famous landmarks, but also have some relaxing days in nature. \
            Would like to keep one day without any activities, just to stay at the hotel and rest.\
            Our budget is moderate, and we prefer shorter travel distances between destinations.
            """
        InferencePipeline().run_inference(sample_user_prompt)

        logger.info('>>>>> Inference completed <<<<<')
        
    except Exception as e:
        logger.exception(e)
        raise e
    
