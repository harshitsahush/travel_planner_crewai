from crewai import Agent
from langchain_community.agent_toolkits.load_tools import load_tools
from tools import *
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(
    api_key = os.getenv("GROQ_API_KEY"),
    model = "llama3-70b-8192"
)

human_tools = load_tools(
    ["human"],
    llm=llm
)


class TravelPlannerAgents:
    # def manager_agent(self, llm):
    #     return Agent(
    #         role='Travel Manager',
    #         goal="""Coordinate the trip to destination ensure a seamless integration of research findings into 
    #             a comprehensive travel report with daily activities, budget breakdown, 
    #             and packing suggestions.""",
    #         backstory="""With a strategic mindset and a knack for leadership, you excel 
    #         at guiding teams towardstheir goals, ensuring the trip not only meets but exceed 
    #         expectations. You also validate your final output before presenting it to the client.""",
    #         verbose=True,
    #         allow_delegation=True,
    #         llm = llm
    #     )
    
    def travel_agent_agent(self, llm):
        return Agent(
            role='Travel Agent',
            goal="""Create the most amazing travel itineraries with budget and 
                packing suggestions for your clients to travel to {destination}.""",
            verbose=True,
            backstory="""Specialist in travel planning and logistics with 
                decades of experience""",
            tools=[CalculatorTools.calculate],
            max_iter=3,                 #so it doesnt run in an infinite loop
            llm = llm
        )
    
    def city_selection_agent(self, llm):
        return Agent(
            role='Cities Selection Expert',
            goal='Select the best cities based on weather, season, and prices',
            verbose=True,
            backstory="""An expert in analyzing travel data to pick ideal destinations""",
            tools=[tavily_search],
            llm = llm,
            max_iter=3
        )

    def local_tour_guide_agent(self, llm):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            verbose=True,
            backstory="""A knowledgeable local guide with extensive information
                about the city, it's attractions and customs""",
            tools=[tavily_search],
            llm = llm,
            max_iter=3
        )
    
    # def quality_control_agent(self, llm):
    #     return Agent(
    #         role='Quality Control Expert',
    #         goal="""Ensure every travel itinerary and report meets the highest 
    #             standards of quality, accuracy, and client satisfaction. 
    #             Review travel plans for logistical feasibility, budget adherence, 
    #             and overall quality, making necessary adjustments to elevate 
    #             the client's experience. Act as the final checkpoint before plans are 
    #             presented to the client, ensuring all details align with the agency's 
    #             reputation for excellence.""",
    #         verbose=True,
    #         backstory="""With a meticulous eye for detail and a passion for excellence, 
    #             you have built a career in ensuring the highest standards in travel 
    #             planning and execution. Your experience spans several years within the 
    #             travel industry, where you have honed your skills in quality assurance,
    #             client service, and problem-solving. Known for your critical eye and 
    #             commitment to excellence, you ensure that no detail, no matter 
    #             how small, is overlooked. Your expertise not only lies in identifying 
    #             areas for improvement but also in implementing solutions that enhance 
    #             the overall client experience. Your role as a quality control expert 
    #             is the culmination of your dedication to elevating travel experiences 
    #             through precision, reliability, and client satisfaction.""",
    #         tools=human_tools,          # builtin tool in langchain, basically a human like
    #         llm = llm
    #     )