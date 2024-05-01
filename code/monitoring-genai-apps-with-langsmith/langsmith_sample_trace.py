from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
llm = AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"), azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), deployment_name="gpt35_turbo", api_version="2024-03-01-preview")
print(llm.invoke("Hello, world!"))