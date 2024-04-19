from semantic_router.layer import RouteLayer, Route
from semantic_router.encoders import AzureOpenAIEncoder
import os
from dotenv import load_dotenv
load_dotenv()

small_talk = Route(
    name="small_talk",
    utterances=[
        "Hey, how are you?", 
        "How's it going?",
        "Nice weather today"
    ],
)

product_questions = Route(
    name="product_questions",
    utterances=[
        "Tell me about the products you offer",
        "What does a keyboard cost?",
        "What does a mouse cost?"
    ],
)

routes = [small_talk, product_questions]
encoder = AzureOpenAIEncoder(api_key=os.getenv("AZURE_OPENAI_API_KEY"), deployment_name="embeddings", azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_version="2024-02-15-preview", model="text-embedding-ada-002")
rl = RouteLayer(encoder=encoder, routes=routes)
print(rl("Hello there").name)
print(rl("What products do you have?").name)