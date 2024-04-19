from semantic_router.layer import RouteLayer, Route
from semantic_router.encoders import AzureOpenAIEncoder
from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()

small_talk = Route(
    name="small_talk",
    utterances=[
        "Hey, how are you?", 
        "How's it going?",
        "Nice weather today",
        "How's your day going?",
        "What's up?",
        "Did you have a good weekend?",
        "How was your weekend?",
        "Any plans for the evening?",
        "How's work/school going?",
        "What have you been up to lately?"
    ],
)

keyboard_questions = Route(
    name="keyboard_questions",
    utterances=[
        "What does a keyboard cost?",
        "What do your keyboards look like?",
        "Are your keyboards mechanical?",
        "What colors do you offer?",
        "Do you have any backlit keyboards?",
        "Can I customize the keycaps?",
        "Are your keyboards compatible with Mac?",
        "Do you offer wireless keyboards?",
        "Are your keyboards ergonomic?",
        "Do you have keyboards with programmable keys?"
    ],
)

mouse_questions = Route(
    name="mouse_questions",
    utterances=[
        "What does a mouse cost?",
        "What do your mice look like?",
        "Are your mice mechanical?",
        "What colors do you offer?",
        "Do you have wireless mice?",
        "Are your mice suitable for gaming?",
        "Can I adjust the DPI settings?",
        "Are your mice compatible with Mac?",
        "Do you offer left-handed mice?",
        "Are your mice Bluetooth enabled?"
    ],
)

routes = [small_talk, keyboard_questions, mouse_questions]
encoder = AzureOpenAIEncoder(api_key=os.getenv("AZURE_OPENAI_API_KEY"), deployment_name="embeddings", azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_version="2024-02-15-preview", model="text-embedding-ada-002")
rl = RouteLayer(encoder=encoder, routes=routes)

@tool
def keyboard_cost() -> str:
    """Used to get pricing information about keyboards"""
    return "You sell keyboards for $75.95 each"

@tool
def keyboard_color_info() -> str:
    """Used to get color information about keyboards"""
    return "Comes in black and white"

@tool
def mouse_cost() -> str:
    """Used to get pricing information about a mouse"""
    return "You sell mice for $49.95 each"

@tool
def mouse_color_info() -> str:
    """Used to get color information about a mouse"""
    return "Comes in black and white"
    

   
def semantic_layer(query: str):
    route = rl(query)
    if route.name == "keyboard_questions":
        model = AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"), azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), deployment_name="gpt35_turbo", api_version="2024-03-01-preview")
        prompt = hub.pull("hwchase17/openai-tools-agent")
        tools = [keyboard_cost, keyboard_color_info]
        agent = create_openai_tools_agent(model, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        agent_executor.invoke({"input": query})
    elif route.name == "mouse_questions":
        model = AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"), azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), deployment_name="gpt35_turbo", api_version="2024-03-01-preview")
        prompt = hub.pull("hwchase17/openai-tools-agent")
        tools = [mouse_cost, mouse_color_info]
        agent = create_openai_tools_agent(model, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        agent_executor.invoke({"input": query})
    else:
        pass
    return query

query = "What does a keyboard cost and what colors does it come in?"
semantic_layer(query)

query = "What does a mouse cost and what colors does it come in?"
semantic_layer(query)