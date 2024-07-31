---
title: "Introduction to LangGraph 🕸️"
date: 2024-07-31T10:00:00-04:00
categories:
  - GenAI
tags:
  - LangChain
  - LangGraph
  - Agents
  - LangSmith
---

{% raw %}<img src="/blog/assets/images/blog_images/introduction-to-langgraph/blog_image.jpg" alt="">{% endraw %}

In this post, I wanted to talk about agentic applications and how [LangGraph](https://langchain-ai.github.io/langgraph/) can help build stateful, multi-actor applications with LLMs. I have personally played around with a few frameworks that help enable agentic applications such as [AutoGen](https://microsoft.github.io/autogen/), [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/concepts/agents?pivots=programming-language-python), and the legacy agent types in [LangChain](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/). I have been intrigued by the promise of LLM agents but have been underwhelmed by the results. Agentic applications are notoriously difficult to control. I have seen multi-agent workflows go ‘off the rails’ and get stuck in a [‘gratification loop’](https://microsoft.github.io/autogen/docs/FAQ#agents-keep-thanking-each-other-when-using-gpt-35-turbo), both making the execution inefficient and wasting tokens. Observability into the agentic workflow was also limited making it a black box to users interacting with them. I have found patterns like [semantic routing](https://schiiss.github.io/blog/genai/guiding-genai-bots-with-semantic-router/) to be far more effective for controlling application flow versus having a comparatively much slower (and more expensive!) LLM determine the flow of the application.

LangGraph claims to offer better control over both the flow and state of your agentic applications and given the other impressive offerings from LangChain (ie: LangSmith) I thought it was worth looking into. These are my initial thoughts after spending a few days building some applications with the framework.

Let’s dive into LangGraph!

## What does Agentic Mean? 🤷‍♂️

To understand the value of LangGraph, we must first understand what it means to be agentic.

An agentic workflow is a process in which an LLM or a series of LLM’s act on behalf of the user to perform tasks. It is a pattern by which we let an LLM determine the flow of the application. Agentic applications exist on a spectrum and there is no hard and fast rule as to what constitutes whether an app is agentic or not. Harrison Chase from LangChain put together a great [blog](https://blog.langchain.dev/what-is-an-agent/) on ‘what is an agent’ and in that blog is a great diagram of the ‘levels of autonomy in LLM applications’.

[![langchain_agentic_levels_of_autonomy](/blog/assets/images/blog_images/introduction-to-langgraph/langchain_agentic_levels_of_autonomy.png)](/blog/assets/images/blog_images/introduction-to-langgraph/langchain_agentic_levels_of_autonomy.png){:target="_blank"}

You will notice numbers 1-4 on the left fall within the ‘human-driven’ category meaning they technically are not ‘agentic’. Even a more advanced pattern like routing is not technically considered agentic. Note numbers 5-6 are considered ‘agent-executed’ since an LLM is heavily leveraged to decide how the system will behave.

Some examples of leveraging an LLM to control the flow of an application could be:

- Using an LLM to route between two potential paths

- Using an LLM to decide which tool to leverage for a given task

- Using an LLM to determine if a given output is sufficient to complete the given task or if more work is required

At the end of the day, this is probably just semantics but it is helpful to understand some general guidelines for what constitutes an agentic application.

Agents also generally have access to tools which can extend an LLM's capabilities. An example of a tool could be a python function that allows the LLM to search the web.

Continuing the example of enabling an LLM to search the web, an input is provided to the agentic app and it determines the input falls outside of it’s training dataset so it must search Bing to get the answer it needs. Below is a diagram that demonstrates a basic agentic workflow.

[![basic_agentic_workflow](/blog/assets/images/blog_images/introduction-to-langgraph/basic_agentic_workflow.png)](/blog/assets/images/blog_images/introduction-to-langgraph/basic_agentic_workflow.png){:target="_blank"}

1. In step one, the user provides input to the agent. This could be 'what is the current weather in New York' for example, which is data the LLM would not know as they do not have access (generally speaking) to real-time data

2. The agent will take the user's input and decide what to do with it. This is where the agentic behavior comes into play and the LLM decides the flow of the application.

3. In this case, our workflow is linear, and we only provide our agent access to one tool, but there could be n number of tools in the agents ‘tool belt’ that can be called upon. A tool could be a basic Python function, and, in this case, the Bing Search tool is a function that leverages the Bing API to make a web search.

4. Finally, a response is returned to the user

Steps 2 and 3 can occur n number of times until the agent determines if the input provided in step 1 is addressed.

## LangGraph's Components 🔨

There are three main components in LangGraph:

1. State: This is a data structure that represents the current snapshot of your application. The schema of the state will be leveraged as input to all nodes and edges in the graph. For example, this could be the chat history in your application and also enables things like [breakpoints](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/breakpoints/?h=breakpoi#how-to-add-breakpoints) for human-in-the-loop scenarios

2. Nodes: Nodes execute work and will emit updates to the state. These are generally Python functions that contain the logic for your agents

3. Edges: These help determine which node should be executed next based on the current state of the application. These are the 'conditionals' of your application

If you follow the [quick start](https://langchain-ai.github.io/langgraph/tutorials/introduction/), in the LangGraph documentation, you will notice a section that leverages IPython to generate the mermaid diagram of the graph:

[![mermaid_diagram](/blog/assets/images/blog_images/introduction-to-langgraph/mermaid_diagram.png)](/blog/assets/images/blog_images/introduction-to-langgraph/mermaid_diagram.png){:target="_blank"}

This visualization is incredibly helpful when designing your agentic application, especially if you are a visual learner.

In short, nodes do the work and edges tell the application what to do next. By combining all these components together we can create complex graphs to orchestrate agentic applications. The algorithm being leveraged by LangGraph is what is referred to as ‘message passing’. In practice, when a node completes an operation, it send’s messages across n number of edges to n nodes depending on the logic.

The interesting part here is you can stream the output of the agentic application throughout the entire workflow to the user. Just to name a few examples, you could stream during state updates or when a node is executing. LangGraph seems to be very flexible in this regard and allows us to keep the user up to date with what step the agentic application is at. The flexibility of the framework is also there since nodes are just Python functions so your imagination is the limit as to what you can build!

## LangGraphs Value Propositions 🫴

There are plenty of other frameworks that help build agentic apps but LangGraph claims to have several core principals that make it the most ‘suitable’ framework for building agentic applications. The principals being controllability, human-in-the-loop, and streaming first.

### Controllability 🎮

LangGraph claims to be 'extremely' low level and gives the developer a high degree of control over the agentic application and from what I have seen thus far, being able to compose nodes and edges provides the developer with a great amount of flexibility. Additionally, being able to visualize the flow in a mermaid diagram allows the developer to wrap their brain around the logic of the app. From my experience leveraging the framework, the graph technology allows the developer more control of the agentic behavior and nodes within the graph are just python functions so it is incredibly customizable.

A notable example I found very helpful to get a sense for the how controllable LangGraph is was the documentation around leveraging [map-reduce branches]( https://langchain-ai.github.io/langgraph/how-tos/map-reduce/).

The reason this example resonated with me is it demonstrated how to distribute workloads across multiple nodes making your agentic application more efficent in terms of runtime.

Map-reduce is a programming model that enables parallel processing and is built into LangGraph. Since there are so many unknowns in agentic applications (ie: edges/conditions are not necessarily known ahead of time), the framework exposes a concept called the [send api](https://langchain-ai.github.io/langgraph/concepts/low_level/#send) which supports conditional edges to address the challenge of not accounting for every scenario or condition your agentic application could take.

The ability to combine many nodes and edges into a graph provides a great amount of flexibility and control over an agentic workflow.

### Human-in-the-Loop 🧑➿

Human-in-the-loop interaction patterns are interesting when it comes to agentic applications. Generally, I have viewed agentic applications in a few contexts:

1. Supervised Actions: This is where a human is ‘in the loop’ and monitors the actions the agentic application will take and provides feedback.

2. Independent Actions: This is where the agentic application is fully autonomous. The app will identify potential actions, execute on them, and the human will review the output. This is an advanced pattern and through my experience building agentic apps, depending on the context of the processes you are trying to automate, there is a lot of risk not having a human-in-the-loop.

LangGraph provides many [examples](https://langchain-ai.github.io/langgraph/how-tos/#human-in-the-loop) for how to create human-in-the-loop workflows and the key concept to understand how they work in LangGraph is called the [checkpointer](https://langchain-ai.github.io/langgraph/concepts/low_level/#checkpointer) which basically allows the human to view the state of the graph and provide feedback on an execution.

### Streaming First 🤖

One of the challenges I have experienced building agentic apps is the lack of visibility into what the agents are doing in the background to accomplish a task. With these types of applications, they can take a while to run and this can be frustrating from a user perspective to not understand what is happening in the background. LangGraph has lots of good [examples](https://langchain-ai.github.io/langgraph/how-tos/#streaming) on how to enable streaming.

AutoGen does support [streaming](https://microsoft.github.io/autogen/docs/notebooks/agentchat_websockets/) however, you need to mess around with IOStream and web sockets to get it working properly. Since LangGraph monitors events at each node and with streaming being built in directly into the framework, I am impressed with how easy it is to enable streaming on your agentic application.

## LangGraph and LangSmith 🤝

So how does LangGraph fit into the larger LangChain stack?

I have stepped through a portion of the [quick start](https://langchain-ai.github.io/langgraph/tutorials/introduction/) tutorial and integrated with LangSmith to take a peek as to what exactly the agentic application is doing in the background. The code for this is located [here](https://github.com/Schiiss/blog/tree/master/code/introduction-to-langgraph/introduction-to-langgraph.ipynb).

I have added markdown annotations to each of the cells to step you through what is going on. We will focus on the last cell in this notebook that launches a chat experience with our agentic application.

[![last_cell](/blog/assets/images/blog_images/introduction-to-langgraph/last_cell.png)](/blog/assets/images/blog_images/introduction-to-langgraph/last_cell.png){:target="_blank"}

Let's ask the question 'search what the weather is in Toronto' and see what the trace looks like in LangSmith.

[![first_trace](/blog/assets/images/blog_images/introduction-to-langgraph/first_trace.png)](/blog/assets/images/blog_images/introduction-to-langgraph/first_trace.png){:target="_blank"}

We can see right off the bat the agentic application did a few things. First, it took the question we provided and determined a tool needed to be called (in this case Tavily Search):

[![second_trace](/blog/assets/images/blog_images/introduction-to-langgraph/second_trace.png)](/blog/assets/images/blog_images/introduction-to-langgraph/second_trace.png){:target="_blank"}

Next, we can see the output from that tool call. In this case, we can see some weather information about Toronto was returned from the API:

[![third_trace](/blog/assets/images/blog_images/introduction-to-langgraph/third_trace.png)](/blog/assets/images/blog_images/introduction-to-langgraph/third_trace.png){:target="_blank"}

And finally, the agentic application comes back with a response:

[![fourth_trace](/blog/assets/images/blog_images/introduction-to-langgraph/fourth_trace.png)](/blog/assets/images/blog_images/introduction-to-langgraph/fourth_trace.png){:target="_blank"}

It is pretty impressive you can log and track all this OOTB using the LangChain stack. These agentic apps have very much been black boxes in the past and it was very difficult to trace what the app did exactly. It is nice to see observability is being given some attention since it is so critical when going into production.

> **_NOTE:_**  One last thing to note in the trace is the amount of tokens leveraged for that request. 808 tokens were leveraged for one basic tool call. Imagine as this scales over time and you start to add more nodes with more edges, with more tools. You really need to keep an eye on your cost when building agentic applications and allowing an LLM to determine the flow of your application.

## Conclusion 🏁

On the surface, LangGraph seems very extendible. Combining the ability to define custom Python functions as nodes and implementing complex conditionals called edges all brought together using a message passing algorithm is impressive. I will need to play around with LangGraph a bit more but it definitely has a lot of promise. The tracing that LangSmith provides is also great for troubleshooting complex agentic workflows. The LangChain stack is growing to become very impressive in it's offerings.

The ability to leverage graphs to build agentic applications provides some key advantages over frameworks such as AutoGen. I was able to wrap my brain around building complex agentic applications using LangGraph since graphs provide a way to visually understand the interactions (ie: nodes and edges) between various steps. Versus leveraging something like AutoGen, where I find it very difficult to visualize the flow/logic of the application, let alone control it.

I will countinue to expirement on the side, however, I think I will still primarily be relying on semantic routers for my production applications. I still view them as faster and more reliable than allowing an LLM to decide the flow of the application. Only time will tell as LLM's become more capable and frameworks like LangGraph become more featured if agents will become the go to pattern when it comes to building 'agentic' type applications.

Thanks for reading!
