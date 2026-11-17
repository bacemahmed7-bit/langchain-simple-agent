import os 
import certifi
import requests

from dotenv import  load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
from langchain.agents import create_react_agent , AgentExecutor


os.environ["SSL_CERT_FILE"] =certifi.where()
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
weatherstack_api_key = os.getenv("WEATHERSTACK_API_KEY")


search_tool = TavilySearchResults(max_results=5)

@tool
def get_weather_data(city : str) -> str:

    """
    fetch current weather information for a city

    """

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={weatherstack_api_key}&query={city}"

    )

    weather_response = requests.get(url)

    data = weather_response.json()

    if "current" not in data:

        return f"Could not Fetch weather data for {city} "



    return (
        f"City : {city} \n"
        f"Temparture : {data['current']['temperature']} °C \n"
        f"Weather descritpion : {data['current']['weather_descriptions']} \n"
        f"Humidity : {data['current']['humidity']} \n"
        f"Wind speed : {data['current']['wind_speed']} \n"
        f"Wind direction : {data['current']['wind_dir']} \n"
        f"Wind degree : {data['current']['wind_degree']} \n"
    )



groq_llm_model =ChatGroq(model="qwen/qwen3.8-27b")
prompt = hub.pull("hwchase17/react")

tools =[search_tool , get_weather_data]

agent = create_react_agent(
    llm=groq_llm_model,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True #see the logs of the agent
)

response = agent_executor.invoke({
    "input" : (
        "What is the capital of Ghana"
        "and then tell me about its current weather"
    )
})

print(response["output"])