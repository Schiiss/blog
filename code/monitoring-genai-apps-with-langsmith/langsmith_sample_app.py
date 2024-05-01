from langchain_core.tools import tool
from langchain_community.utilities import BingSearchAPIWrapper
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

embedding_function = AzureOpenAIEmbeddings(
    azure_deployment="embeddings",
    openai_api_version="2023-05-15",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

llm = AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"), azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), deployment_name="gpt35_turbo", api_version="2024-03-01-preview")

#Web Search Tool
@tool
def web_search(search_query: str) -> str:
    "Use the web to search"
    search = BingSearchAPIWrapper()
    return search.run(search_query)

#Search LangSmith Docs
@tool
def search_langsmith_docs(search_query: str) -> List[str]:
    "Search LangSmith docs"
    db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    docs = db3.similarity_search(search_query, k=2)
    page_contents = []
    for doc in docs:
        page_contents.append(doc.page_content)
    return page_contents

#Add tools to array
tools = [web_search, search_langsmith_docs]

#Sample prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

#Provide sample inputs
agent_executor.invoke({"input": "using the langsmith docs, can you tell me what tags are?"})
agent_executor.invoke({"input": "using bing, can you tell me what langsmith tags are?"})
agent_executor.invoke({"input": "can you tell me what tags are?"})