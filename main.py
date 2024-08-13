from agents import TravelPlannerAgents
from tasks import TravelPlannerTasks
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from crewai import Crew, Process


agents = TravelPlannerAgents()
tasks = TravelPlannerTasks()

load_dotenv()
llm = ChatGroq(
    api_key = os.getenv("GROQ_API_KEY"),
    model = "llama3-70b-8192"
)

# setup agents
# manager_agent = agents.manager_agent(llm)
travel_agent = agents.travel_agent_agent(llm)
city_selection_agent = agents.city_selection_agent(llm)
# quality_control_agent = agents.quality_control_agent(llm)

# setup tasks
# manager_task = tasks.manager_task(manager_agent)
select_cities = tasks.select_cities(city_selection_agent)
gather_cities_info = tasks.gather_cities_info(city_selection_agent)        
plan_itinerary = tasks.plan_itinerary(travel_agent)                   
# quality_control = tasks.quality_control(quality_control_agent)            


#setup tools --- done


#add all
crew = Crew(
    agents = [travel_agent, city_selection_agent],
    tasks = [select_cities, gather_cities_info, plan_itinerary],
    process = Process.sequential,               #in sequential, output of previous process is automatically passed to next
    verbose = True
)

results = crew.kickoff()
print(results)

with open("final_iti.txt", "w") as file:
    file.write(str(results))