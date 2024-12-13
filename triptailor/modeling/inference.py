from loguru import logger
from agent import Agent
from dotenv import load_dotenv

_ = load_dotenv()

from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI

class InferencePipeline:
    def __init__(self):
        pass

    def main(self):           
        with SqliteSaver.from_conn_string(":memory:") as memory:

            prompt = """
            I am planning a 3-day family trip to Italy. We enjoy historical sites, good food, and outdoor activities. \
            We’d like to visit different cities and explore famous landmarks, but also have some relaxing days in nature. \
            Would like to keep one day without any activities, just to say at the hotel and rest.\
            Our budget is moderate, and we prefer shorter travel distances between destinations.
            """
            #tool = TavilySearchResults(max_results=2)
            model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            agent = Agent(model, system=prompt, checkpointer=memory)
            thread = {"configurable": {"thread_id": "1"}}
            response = []

            logger.info("Streaming the responses")
            for s in agent.graph.stream({'user_query': prompt}, thread):
                print(s)
                response.append(s)
            logger.info("Streaming ended")


if __name__ == "__main__":
    try:
        logger.info('>>>>> Inference started <<<<<')

        inference_pipeline = InferencePipeline()
        inference_pipeline.main()

        logger.info('>>>>> Inference completed <<<<<')
        
    except Exception as e:
        logger.exception(e)
        raise e
    
