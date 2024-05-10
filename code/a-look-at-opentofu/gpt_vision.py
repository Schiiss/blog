from dotenv import load_dotenv
load_dotenv()
import os
import base64
from mimetypes import guess_type
from openai import AzureOpenAI

# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

# Example usage
image_path = 'C:\\Users\\conne\\development\\repos\\blog\\assets\\images\\blog_images\\a-look-at-opentofu\\azure_architecture.png'
data_url = local_image_to_data_url(image_path)
print("Data URL:", data_url)

api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key=os.environ.get("AZURE_OPENAI_KEY")
deployment_name = 'vision'
api_version = '2023-12-01-preview' # this might change in the future

client = AzureOpenAI(
    api_key=api_key,  
    api_version=api_version,
    base_url=f"{api_base}openai/deployments/{deployment_name}/extensions",
)

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        { "role": "system", "content": "You are a helpful assistant that analyzes azure architectures" },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": "Describe this architecture and generate terraform code to deploy it:" 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }
        ] } 
    ],
    extra_body={
        "dataSources": [
            {
                "type": "AzureComputerVision",
                "parameters": {
                    "endpoint": os.environ.get("COMPUTER_VISION_ENDPOINT"),
                    "key": os.environ.get("COMPUTER_VISION_KEY")
                }
            }],
        "enhancements": {
            "ocr": {
                "enabled": True
            },
            "grounding": {
                "enabled": True
            }
        }
    },
    max_tokens=2000
)
print(response)