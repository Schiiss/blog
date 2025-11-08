---
title: "🤖 Databricks MCP Catalog: The Missing Operational Layer for Enterprise Agents"
date: 2025-10-17T10:00:00-04:00
categories:
  - GenAI
tags:
  - Databricks
  - MCP
  - Enterprise AI
  - Data Platforms
---

{% raw %}<img src="/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/blog_image.png" alt="">{% endraw %}

The amount of adoption and hype around **Model Context Protocol (MCP)** has pleasantly surprised me lately. While I was skeptical at the start regarding its value proposition, I'm now seeing how it's coming together.

The most important aspect of agents are their **tools**, as they give them access to your enterprise context as well as the outside world. These tools empower agents to perform actions, and I'm starting to see how MCP will enable more seamless agent integration with the outside world.

At Plains, we've fully embraced the **Lakehouse architecture**, and the possibilities expand dramatically when you have data from your critical applications centralized in one place. This presents some fascinating opportunities for MCP, which I'll explore in detail below.

Databricks has been releasing lots of exciting features during their ‘Week of Agents’ campaign and I wanted to cover their recent release around the [MCP catalog and marketplace](https://www.databricks.com/blog/accelerate-ai-development-databricks-discover-govern-and-build-mcp-and-agent-bricks?utm_source=bambu&utm_medium=social&utm_campaign=advocacy&blaid=8065278).
I wanted to put together a short blog post on how to get started and where I see some opportunities.

---

## 📢 Announcements

There were a few exciting announcements around MCP during this release, but it really boils down to discovery, governance, and actionability of MCP endpoints. On the discovery side, you can now explore external MCP servers via the marketplace:

[![External MCP Catalog](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/extrernal_mcp_marketplace.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/extrernal_mcp_marketplace.png)

There are some neat MCP integrations to S&P and Nasdaq and there are a few free ones to get started with. I will cover the easiest way to explore external MCP shortly.

You can also more easily discover MCP servers hosted within your environment. Agent Bricks makes building agents easier than ever, opening up agent development to a wide variety of personas and enabling ‘citizen developers’ to explore what MCP servers are leverageable today within your Databricks environment.

Similar to traditional data products, discoverability is an important attribute of them, and I see MCP servers becoming products within your data and AI platform that will start to take on a lifecycle of their own.

You can now explore MCP servers within your environment in the 'Agents' tab:

[![Discover MCP Servers](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/discover_mcp_servers.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/discover_mcp_servers.png)

Lastly, the Multi-Agent supervisor now supports connecting to external MCP servers, giving agents access to AI-ready external data. I fully expect the offerings in this catalog to expand in the future.

[![MAS External MCP](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_external_mcp.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_external_mcp.png)

---

## 🚀 Getting Started

I would say the easiest way to get started with testing some of these new features is to select one of the free external MCP servers. I suggest the Tavily MCP that allows agents to hook into the web.

1. Navigate to [Tavily](https://app.tavily.com/) and create an account. You get 1000 free API calls a month to test out the functionality!
2. Next, navigate to the Databricks Marketplace and find the Tavily MCP server and select 'Install'.

   [![Tavily Marketplace Setup Step 1](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_1.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_1.png)

3. Finally, place your API key from [Tavily](https://app.tavily.com/) into the bearer token input and click 'Install'.

   [![Tavily Marketplace Setup Step 2](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_2.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_2.png)

4. You should now be able to see your newly created Tavily MCP server in the catalog:

   [![Tavily Marketplace Setup Step 3](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_3.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_3.png)

5. Now the fun part begins and we can create a multi-agent supervisor and give it access to the new MCP server:

   [![Tavily Marketplace Setup Step 4](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_4.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_4.png)

6. Asking the agent in the playground, `what tools do you have access to?` is a good first test to make sure the agent has access to be able to interact with the Tavily MCP server:

   [![Tavily Marketplace Setup Step 5](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_5.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/tavily_marketplace_step_5.png)

7. Let's give the agent a run for its money and ask a tough question:

   > For companies in the midstream oil & gas sector, what are the top three real-world use cases where multi-agent systems have reached production? Include provider names, architecture patterns, and ROI details if available.

   The agent seems to spin for about a minute, but no answer is returned:

   [![First MAS Question](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_first_question.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_first_question.png)

   The trace also does not seem to indicate that the Tavily MCP server was called; however, I can see the calls on my Tavily subscription.

   [![First MAS Question Trace](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_first_question_trace.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_first_question_trace.png)

8. Let's try another question!

   > How does the Model Context Protocol (MCP) differ from OpenAI Function Calling?

   This one worked really well. I can see in the MLflow trace that the Tavily MCP server was called multiple times to generate a file response:

   [![Second MAS Question Trace 1](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_second_question_trace_1.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_second_question_trace_1.png)

   [![Second MAS Question Trace 2](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_second_question_trace_2.png)](/blog/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas_second_question_trace_2.png)

   I am also impressed with the answer. For reference, you can view [agents response](https://github.com/Schiiss/blog/blob/master/assets/images/blog_images/databricks-mcp-catalog-the-missing-operational-layer-for-enterprise-agents/mas-mcp-vs-openai-functions-response.md) to my second question to see how it did.

> **Note**: I have converted the response to markdown for better readability.

---

## 💡 Use Case(s)

I’ll admit, some of the MCP use cases in the market right now still feel a bit aspirational. But I think that’s the point: the value comes before the use case. Getting ahead of the curve on how systems will be accessed by agents and ensuring your data is structured, cataloged, and centralized is what positions you to move fast when the patterns become clear.

Instead of waiting for the “perfect” GenAI use case to fall into our lap, the strategy is:

- Get the prerequisites in place now
- Data centralized
- Metadata and governance clean
- Services exposed consistently through something like MCP

Then iterate on use cases as the opportunities show up.

One area where this does feel tangible today is with the sensor data we collect from our pipelines. We are already well underway a build out of an anomaly detection layer (both a rules-based engine and an ML classifier, e.g., XGBoost). But once an anomaly is flagged, an operator still has to go and validate whether it is real or explainable. This is a highly manual workflow that often requires switching between SCADA, historian data, Maximo, and inspection/maintenance logs.

An MCP-connected agent could replicate the exact steps an experienced operator takes to triage the anomaly but do it in seconds instead of minutes or hours.

### The Agent’s Workflow

Once an anomaly is detected, the agent would:

1. **Automatically trigger from the alert**
    - Input comes from the classifier/rule engine
    - Pass along signal metadata (location, severity, timestamp, sensor type)
2. **Check maintenance history via Maximo**
    - “Is there a work order already open for the affected equipment?”
    - If yes → annotate the alert as operationally explained
3. **Query SCADA / historian for recent operating patterns**
    - Compare pressures/flows/temperatures before and after anomaly
    - Detect step changes vs gradual drift vs sensor noise patterns
4. **Look at nearby related assets**
    - Sometimes upstream equipment explains downstream anomalies
    - Check if other components in the same block also changed state
5. **Retrieve relevant inspection or ILI records**
    - Determine if this area has prior corrosion, fatigue, or coating damage history
6. **Return a structured human friendly report**

    Example output:

    > Anomaly at Station 12 Compressor Train B.
    > No active work order. Upstream suction pressure dropped 8% at the same timestamp, possibly due to upstream supply swings. Last ILI shows no integrity red flags. Recommend monitoring; no immediate action required.

The cool part with this potential use case is MCP standardizes how agents access enterprise systems, and with MCP servers discoverable via the MCP catalog, other agent builders can tie into existing functionality.

---

## 🎯 Conclusion

The introduction of the MCP catalog and marketplace represents a significant step forward in making enterprise AI agents more accessible and operational. By providing a centralized hub for discovering, managing, and utilizing MCP servers, Databricks is addressing key challenges in enterprise agent development. As the ecosystem grows and more organizations contribute their MCP servers, we'll likely see an acceleration in the adoption of agent-based solutions across industries.

It would be really neat if eventually these MCP servers were also exposed in Databricks One for the business to discover agents and the tools they can access.

These features are still in beta, so it is fully expected to run into the issue we saw in the 'Getting Started' section where the agent did not reply at all. I am excited to see where this goes next.

Thanks for reading! 🙂
