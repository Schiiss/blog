---
title: "Building an Agentic Personal Assistant 🤖"
date: 2024-11-12T10:00:00-04:00
categories:
  - GenAI
tags:
  - LangChain
  - LangGraph
  - Agents
---

{% raw %}<img src="/blog/assets/images/blog_images/building-an-agentic-personal-assistant/blog_image.png" alt="">{% endraw %}

There are many things in our lives that are tedious and mundane that can be made easier with automation. Generative AI opens interesting opportunities for automation since we can combine traditional automation methods (ie: scripts) with a generative AI interface. The power of putting a generative AI interface on top of traditional automation enables natural language interaction, allowing the agent to reason about which function or tool to use.

I started thinking of tasks in my own life that could be automated. I wanted to start small, thinking of small tasks throughout my day that could be easily automated and start building off that into a framework where I can build my own scalable personal assistant.

Imagine an AI-powered assistant that not only automates repetitive tasks but does so intuitively, choosing tools and workflows based on what you ask in plain language. In this post, I’ll walk you through building a simple but scalable personal assistant using [LangGraph](https://langchain-ai.github.io/langgraph/), which intelligently handles registration tasks for visitor parking at my apartment building.

Let’s jump into a quick overview about what it means to be agentic.

> **_NOTE:_**  While the code for this is open source, I have generalized the license plates and obfuscated the unique parking codes for obvious reasons. With that being said, the code will not run without these unique values and the code has been published purely to demonstrate the implementation pattern.

## What does it mean to be Agentic? 🤷‍♂️

Like I talked about in my [Introduction to LangGraph](https://schiiss.github.io/blog/genai/introduction-to-langgraph/#what-does-agentic-mean-%EF%B8%8F) blog, 'An agentic workflow is a process in which an LLM or a series of LLM’s act on behalf of the user to perform tasks'.

In the example we are about to step through, we leverage an 'LLM to decide which tool to leverage for a given task' and help us automate the registration of visitor vehicles.

## Use Case

At a high-level, I wanted to automate the registration of visitor vehicles at my building.

The apartment building I live in requires all visitors to register their license plate. The parking application requires a few inputs:

- Location #: A unique identifier for the building I live in

- Code: A unique password/code that identifies me

- License Plate: The plate of the visitor

- Name: Name of the visitor

- Phone Number: Phone number of the visitor

Each time I navigate to the parking application, it does not remember my location number, code, or maintain a list of frequent visitors to my apartment. It gets tedious to have to enter in all these fields manually.

I wanted to develop something that could automate registering visitor vehicles when they come to my apartment. Let’s dive into the implementation of this use case.

## Reverse Engineering the Parking Applications API

The application my building uses to register plates is [offstreet.io](https://www.offstreet.io/). Unfortunately, offstreet.io does not have an officially supported API. This means we will have to get our hands dirty and open the [developer tools](https://developer.chrome.com/docs/devtools) in chrome, reverse engineer the API's, and eventually mock them in Python.

Since we must reverse engineer the API, we need to first enter in all our inputs manually to ensure we capture all the required API calls to register a plate. After entering in the location number, code, license plate etc. it brings us to this screen.

[![registered_plate](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/registered_plate.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/registered_plate.png){:target="_blank"}

Note, I have been monitoring the API calls offstreet makes throughout the whole registration process to try and identify the API call we need to mock. There is not an exact science to these sort of things and to identify the right API call to mock required lots of clicking around in the network tab in chrome and leveraging tools like [postman](https://www.postman.com/), a great tool to make API calls.

Eventually through some trial and error I found the API call ‘register’ that combines all the inputs previously entered into the form and send it to the endpoint https://ogr-api.offstreet.io/v2/portal/registration.

[![register_api_call](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/register_api_call.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/register_api_call.png){:target="_blank"}

Opening the JSON payload of that API call, I can see all the parameters that the API expects.

[![register_api_call_payload](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/register_api_call_payload.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/register_api_call_payload.png){:target="_blank"}

I also want to get a notification when my personal assistant successfully registers a plate. Adding my email and clicking send on the UI should reveal the API call I need to mock:

[![email_notification](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/email_notification.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/email_notification.png){:target="_blank"}

I can now see the API call the application made in chrome developer tools along with the request URL and payload structure.

[![email_notification_api](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/email_notification_api.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/email_notification_api.png){:target="_blank"}

[![email_notification_api_payload](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/email_notification_api_payload.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/email_notification_api_payload.png){:target="_blank"}

Now that we have identified the right API's to use and what parameters to pass in, we can mock the calls in Python.

```python
def register_plate(license_plate: str, parker_name: str, parker_number: str) -> str:
    """Register a car with parking service"""
    config_id = int(os.getenv("CONFIG_ID", "").strip())
    location_id = int(os.getenv("LOCATION_ID", "").strip())
    tenant_id = int(os.getenv("TENANT_ID", "").strip())
    state = os.getenv("STATE", "").strip()
    parking_code = os.getenv("PARKING_CODE", "").strip()
    parker_name_id = int(os.getenv("PARKER_NAME_ID", "").strip())
    parker_contact_number_id = int(os.getenv("PARKER_CONTACT_NUMBER_ID", "").strip())
    contact_email = os.getenv("CONTACT_EMAIL", "").strip()
    url = "https://ogr-api.offstreet.io/v2/portal/registration"
    payload = json.dumps({
        "configId": config_id,
        "locationId": location_id,
        "tenantId": tenant_id,
        "vehicle": {
            "plate": license_plate,
            "state": state
        },
        "code": parking_code,
        "timeRaw": {
            "start": "2024-03-11T22:47:00.000Z",
            "end": "2024-03-12T22:47:00.000Z",
            "durationInMinutes": 1440
        },
        "additionalFieldValues": [
            {
                "id": parker_name_id,
                "label": "Parker Name",
                "value": parker_name,
                "additionalField": {
                    "id": parker_name_id
                }
            },
            {
                "id": parker_contact_number_id,
                "label": "Contact Number",
                "value": parker_number,
                "additionalField": {
                    "id": parker_contact_number_id
                }
            }
        ],
        "ignoreExistingRegistration": True
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    confirmation_number = response_dict.get('confirmation')
    if confirmation_number:
        conf_url = f"https://ogr-api.offstreet.io/v2/portal/registration/{confirmation_number}/sendParkingConfirmationEmail"
        payload2 = json.dumps({"recipient": contact_email})
        requests.post(conf_url, headers=headers, data=payload2)
        return "Plate Registered"
    else:
        print(f"Error: {response_dict}")
        return "Registration failed"
```

I have open-sourced the code for that [here](https://github.com/Schiiss/blog/tree/master/code/building-an-agentic-personal-assistant/offstreet_api.ipynb).

## Adding Agentic Capabilities 🤖

Now that we have mocked the API calls necessary to register a plate and get a notification, I want to integrate these Python functions with an agentic framework so I can in natural language, register a visitors plate. I have decided to leverage [LangGraph](https://langchain-ai.github.io/langgraph/) for this use case.

As always, I have [open-sourced](https://github.com/Schiiss/blog/tree/master/code/building-an-agentic-personal-assistant/personal_assistant.ipynb) the code if you want to go and have a look!

Since we have mocked our API calls in Python, it is very easy to integrate it into LangGraph. In this case, I am going to leverage the [ReAct agent](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/#react-implementation) since we are going to want out application to select between a few tools to register a plate.

The agent will be structured like this where it will take in some input (visitor information) and will select from a series of tool until the agent determines that the user's input has been addressed.

[![agent_nodes](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/agent_nodes.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/agent_nodes.png){:target="_blank"}

Since we want to interact with the agent in natural language, we must enable the agent to be able to pass the necessary parameters (ie: license_plate, parker_name ,parker_number) dynamically. So if we were to pass ‘register Alex Johnson's plate’ to the agent, how would it pull that visitors necessary information?

The way I addressed this problem was by creating a plates.csv file with all the parameters necessary to register a visitor’s plate. I created a [sample CSV](https://github.com/Schiiss/blog/tree/master/code/building-an-agentic-personal-assistant/plates.csv) to show what this looks like:

```csv
name,plate,number
John Doe, ABC123, 555-0123
Jane Smith, XYZ789, 555-9876
Alex Johnson, LMN456, 555-3456
```

I then gave my agentic application access to read said CSV by creating another tool to extend it’s capabilities.

```python
@tool
def get_license_plate():
    """Does a lookup for the license plate based on the persons name"""
    try:
        data = []
        with open('plates.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"Error: File 'plates.csv' not found.")
        return None
```

The agent can now use this tool to do a look up of a visitors license plate. For example, let's ask the agent to ‘register Alex Johnson's plate’:

[![agentic_register_plate_1](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/agentic_register_plate_1.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/agentic_register_plate_1.png){:target="_blank"}

You will notice a few things in the above screenshot.

1. We passed through out input as natural language with no further details besides the visitors name

2. The agent tried to register the plate by passing through incorrect parameters

3. The agent got a 400 response back from the API

4. The agent determined that it needs to use the ‘get_license_plate’ tool first to read the CSV data

Scrolling down to the bottom of the output, the agent takes the inputs pulled from the CSV and passes them successfully to the 'register_plate' tool

[![agentic_register_plate_2](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/agentic_register_plate_2.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/agentic_register_plate_2.png){:target="_blank"}

Finally, I receive an email with the registration details:

[![email_confirmation](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/email_confirmation.png)](/blog/assets/images/blog_images/building-an-agentic-personal-assistant/email_confirmation.png){:target="_blank"}

As mentioned earlier, we are leveraging the ReAct framework for our agent. The [ReAct](https://arxiv.org/pdf/2210.03629) (Reasoning and Acting) approach is particularly well-suited for agent-based implementations because it enables agents to manage complex tasks by reasoning through decisions before taking actions. Here’s why ReAct shines in this setup:

1. Stepwise Reasoning: ReAct allows the agent to break down tasks into smaller steps, combining logical reasoning with action-taking. This capability is beneficial when an agent needs to analyze or clarify its goal and consider which specific tools or information sources to use—perfect for tasks that require a few layers of information retrieval or validation, like checking visitor information in your parking registration case.

2. Dynamic Task Switching: By interleaving reasoning steps with actions, ReAct agents can adaptively switch tasks based on intermediate results. For example, if the agent needs more information before it can complete the registration (e.g., visitor details), it can dynamically choose to access the get_license_plate tool before attempting to register the plate. This ability to change course based on partial outcomes makes ReAct ideal for handling workflows that don’t follow a strictly linear sequence.

3. Minimizing Errors and Reattempts: Traditional automation often moves sequentially through predefined steps, which can result in errors if specific conditions aren't met. ReAct agents, however, can interpret errors (like a 400 response) as an indicator to try alternative actions. For example, when the agent receives a response indicating missing information, it can reason that it should consult the CSV lookup tool to retrieve complete data before reattempting registration.

4. Natural Language Interface: ReAct’s reasoning capability aligns well with natural language commands. When given a vague or partial instruction (like “register Alex Johnson's plate”), the ReAct agent can parse the request, identify that it lacks some information, and decide which tools to use to fill in the gaps. This allows for more intuitive, human-like interactions with the assistant.

In essence, ReAct helps the agent think critically about “what to do next” rather than merely following a script, which makes it a robust choice for applications where user intent and task requirements may vary from instance to instance. This flexibility brings AI closer to being an effective personal assistant, capable of problem-solving in real time.

## Conclusion 🏁

I hope this implementation offers a concrete example of how generative AI can transform small and repetitive tasks in our lives. With this approach, there’s potential to scale up to more complex tasks, broadening the assistant's utility as an agent capable of managing more aspects of daily life.

As a next step, I plan to dockerize and expose this application as an API that I can integrate with Alexa to automate this process further.

Thanks for reading 😊
