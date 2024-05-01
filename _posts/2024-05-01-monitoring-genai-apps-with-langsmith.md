---
title: "Monitoring GenAI Apps with LangSmith 👀🦜"
date: 2024-05-01T10:00:00-04:00
categories:
  - GenAI
tags:
  - LangChain
  - LangSmith
  - DevOps
  - OpenAI
---

{% raw %}<img src="/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/bot_monitoring.jpeg" alt="">{% endraw %}

The hype cycle around GenAI is still going strong and companies are trying to figure out how to best leverage the tech to help with their businesses. Amongst the hype, I think it is easy forget the age old practices and principles decades of software development has taught us. It is easy to neglect fundamentals such as the DevOps principals that can help take these GenAI applications into a production ready state.

There are many important components to the DevOps lifecycle:

![Devops](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/DevOps.jpg)

In this blog post, the primary focus lies on the critical aspects of 'monitoring', 'coding', and 'testing' within the DevOps lifecycle concerning the development of applications integrating Generative AI functionalities. It aims to address challenging questions from users such as, "When the 'bot' delivers an unexpected response, how can we precisely trace the sequence of actions executed by the agents?" Such inquiries underscore the indispensable role of a robust monitoring solution in effectively managing and troubleshooting complex AI-driven systems.

As I've been rolling out these apps into the wild, I've been bombarded with questions like the ones I mentioned earlier. So, I started tinkering with LangChain's tool for testing and monitoring GenAI apps, known as [LangSmith](https://docs.smith.langchain.com/user_guide). With LangSmith now being offered in the [Azure Marketplace](https://blog.langchain.dev/announcing-langsmith-is-now-a-transactable-offering-in-the-azure-marketplace/), the barrier to entry to leverage tools like these in an enterprise setting is becoming lower and lower.

## What is LangSmith? 🤷‍♂️

According to the [LangSmith documentation](https://docs.smith.langchain.com/user_guide), ‘LangSmith is a platform for LLM application development, monitoring, and testing.’. I have personally used LangSmith with a couple projects and I found it incredibly useful for debugging things like 'infite loops' when you are working with things like multi turn agents, logging interactions with the bot, using it for fine-tuning, and capturing user feedback. LangSmith helps to answer questions like:

- How do I ensure outputs remain deterministic as my prompts evolve over time?
- How does mixing and matching different models affect my outputs?
- What happened when a particular prompt was passed through?
- What was the cost (ie: tokens) for a particular run?
- Are user's satisfied with the LLM's output?

LangSmith reminds me a lot of [Azure Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview) where just by adding an instrumentation key to your app, lots of insightful telemetry is enabled for you by default. It is very easy to get started but takes time to master!

Let's jump in and get LangSmith set up to understand how it works!

## LangSmith Setup ⚙️

LangSmith is very easy to setup and is exposed as a [PyPI Package](https://pypi.org/project/langsmith/) for easy installation.

First, let's create and activate a python virtual environment and install dependencies. Note, the requirements.txt for this code can be found [here](https://github.com/Schiiss/blog/tree/master/code/monitoring-genai-apps-with-langsmith/requirements.txt) for your reference.

```powershell
python -m venv venv
venv\scripts\activate
pip install -r requirements.txt
```

Now that our environment is set up, let's create a program that will interact with OpenAI's GPT-3.5 model, send a prompt, and log the interaction in LangSmith. Below is a sample of my environment file, and I want to draw your attention to a few settings:

- LANGCHAIN_ENDPOINT: This is the LangSmith API Endpoint
- LANGCHAIN_API_KEY: LangSmith API Key Generated on your account
- LANGCHAIN_PROJECT: LangSmith project to send the traces

The above setting will enable tracing of your application in LangSmith.

To generate an API key, navigate to the [LangSmith portal](https://smith.langchain.com/), navigate to settings, and select API Keys:

![Generate_API_Key](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/generate_key.png)

Generate an API key and place it in your environment file using the LANGCHAIN_API_KEY key. Once the API key is added to your environment file, let's run the below code:

```python
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

llm = AzureChatOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"), azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), deployment_name="gpt35_turbo", api_version="2024-03-01-preview")
print(llm.invoke("Hello, world!"))
```

Let's jump in to LangSmith and have a look at the trace that appeared after running our code.

![New_Trace](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/new_langsmith_entry.png)

As you can see, it is incredibly easy to 'instrument' your application and send the logs to LangSmith. In the subsequent sections, I would like to dive a bit deeper into the various offerings in LangSmith like debugging, capturing user feedback, and fine-tuning! By no means will this be exhaustive, but I would like to provide an overview.

## LangSmith in Practice ⚽

I have created a sample application to demonstrate the capibilites of LangSmith and have open sourced it [here](https://github.com/Schiiss/blog/tree/master/code/monitoring-genai-apps-with-langsmith/langsmith_sample_app.py). At a high-level, the application does the following:

![Sample_App](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/sample_langsmith_app.png)

The user will send in some input to an agent that will then route to the tool the agent thinks will resolve the user's input. In this case, I have provided the agent with two tools:

1. web_search - Has access to the bing search API
2. search_langsmith_docs - Will have access to a select few chunked and vectorized pages from the LangSmith documentation

For the search_langsmith_docs tool, I had to first chunk and vectorize a few web pages from their documentation. I have open sourced the code I leveraged to do just that. You can find that [here](https://github.com/Schiiss/blog/tree/master/code/monitoring-genai-apps-with-langsmith/langsmith_docs_pipeline.py). You will notice, I have leveraged a few of LangChains abstractions to load the web pages into ChromaDB.

After running the above code, I can see the documents in ChromaDB and we are good to start using the search_langsmith_docs tool:

![chroma_query](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/chroma_db_query.png)

The web_search tool works out of the box and only requires a Bing search API key so no additonal setup is required. I have created a [resource](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource) in Azure for it.

### Anatomy of a Trace 🫀

Let's run our application and pass through a few different queries:

1. using the langsmith docs, can you tell me what tags are?
2. using bing, can you tell me what langsmith tags are?
3. can you tell me what tags are?

A trace in LangSmith provides many interesting data points. Looking at the first query, we can see a few important metrics right away which I have annotated below:

![Query1_Trace](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/query_1_trace.png)

Note, all of these metrics are out of the box, and come as soon as you add the LangSmith API key to your app.

Let's walk through a few scenarios where these traces prove helpful.

### Troubleshooting LLM Output 🤔

I've come across inquiries from end users who are using live applications, which resemble the following: "The bot provided an unexpected answer. What might have caused this?" To effectively answer this question, we need to dig into the logs, or in this case, the LangSmith traces to understand what the agent decided to do based on user input. Let's say the users input was 'can you tell me what tags are?' and they did not receive the answer they would expect.

Going through my troubleshooting steps, the first thing I would likely do is see if the underlying data the agent has access to, even contains information about a tag in LangSmith. If the agent has not been grounded in the relevant data, we know the response back will not contain the information the user is looking for. In this case, we know the agent does via the search_langsmith_docs tool we created earlier, so what else could be the problem?

Having a look at the trace I can see a few things:

1. There is no reference to information from the LangSmith documentation. Ie: 'Tags are collections of strings that can be attached to runs'
2. No tool was selected. In other words, the agent decided not to use the web_search tool or the search_langsmith_docs tool and come up with an answer purely based on the data it was trained on.

![No_Tool_Selected](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/no_tool_selected.png)

It seems since the input from the user was not explicit, the agent did not select a tool, therefore, relying on the data the LLM was trained on. This data will not be up to date with the LangSmith documentation.

Let's contrast with the query 'using the langsmith docs, can you tell me what tags are?', and we can see the agent actually selected the search_langsmith_docs tool and was able to retrieve some relevant information from ChromaDB via a RAG pipeline:

![Tool_Selected](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/tool_selected.png)

Some next steps could be working with the user on how to use effective prompt engineering techniques, or abstracting that from the user in the software by leveraging a methodology such as the [MultiQueryRetriever](https://python.langchain.com/docs/modules/data_connection/retrievers/MultiQueryRetriever/) to rewrite the input in a few different ways to optimize for RAG.

### Soliciting Feedback From Users ✅❌

LangSmith can also be leveraged to capture [feedback](https://docs.smith.langchain.com/cookbook/feedback-examples) from the users. The most basic implementation of this would be a thumbs up/thumbs down rating system that is exposed at the end of an interaction with an LLM. LangSmith has an example of this using [streamlit](https://docs.smith.langchain.com/cookbook/feedback-examples/streamlit).

To demonstrate this, I have manually annotated a run and filtered by it:

![Feedback](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/feedback.png)

As we will see in the next section, this feedback can be collected into a dataset for fine-tuning operations.

### Fine-Tuning 🔨

Building off of the solicitation of user feedback, and seeing we can filter the feedback, what we can do is take the inputs and outputs of those runs in LangSmith and add them to a dataset.

![Add_To_Dataset](/blog/assets/images/blog_images/monitoring-genai-apps-with-langsmith/add_to_dataset.png)

Subsequently, you can export the same dataset as a JSONL file, which can then be uploaded to Azure OpenAI for [fine-tuning a model](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython-new&pivots=programming-language-studio).

The act of fine-tuning is heavily supported by papers/blogs like what LangChain describes [here](https://blog.langchain.dev/chatopensource-x-langchain-the-future-is-fine-tuning-2/) underscoring both cost savings and performance enhancements. This feature in LangSmith facilitates seamless data collection and fine-tuning of models.

## Conclusion

Through my experimentation with LangSmith, I've found it to be a valuable tool for streamlining DevOps processes in the development of GenAI-enabled applications. While we've only scratched the surface of its potential, I'm optimistic about its ability to enhance the development lifecycle.

LangSmith boasts an active community, and its official [YouTube channel](https://www.youtube.com/watch?v=4rupAXVraEA&list=PLfaIDFEXuae0bYV1_60f0aiM0qI7e1zSf), regularly shares updates and tutorials, fostering a supportive environment for users.

As we navigate the complexities of integrating GenAI into our applications, it's essential not to overlook foundational principles like DevOps. LangSmith offers insights into critical aspects of monitoring, coding, and testing within this framework, addressing challenges such as tracing unexpected responses and managing complex AI-driven systems effectively.

With LangSmith now available in the Azure Marketplace, its accessibility for enterprise adoption continues to grow, lowering the barriers to leveraging such tools effectively.

Thanks for reading.