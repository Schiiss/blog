---
title: "📈🚀 Where I’m Getting the Most Value from Generative AI Today: Batch Inference at Scale"
date: 2025-09-13T10:00:00-04:00
categories:
  - GenAI
tags:
  - Databricks
---

{% raw %}<img src="/blog/assets/images/blog_images/where-im-getting-the-most-value-from-generative-ai-today-batch-inference-at-scale/blog_image.png" alt="">{% endraw %}

I have found myself in a rollercoaster of emotions over the past two years during this AI Hype cycle. There is a visual model called the ‘Gartner Hype Cycle’ that has been catching on, namely in the AI community. It articulates the various stages of hype as a given technology matures.

[![Gartner Hype Cycle](/blog/assets/images/blog_images/where-im-getting-the-most-value-from-generative-ai-today-batch-inference-at-scale/gartner_hype_cycle.jpg)](/blog/assets/images/blog_images/where-i’m-getting-the-most-value-from-generative-ai-today-batch-inference-at-scale/gartner_hype_cycle.jpg)

I have been guilty in the past of riding the hype cycle and inflating my expectations of what the technology can do.

I have found myself in the ‘trough of disillusionment’ a few times over the past year, especially as I have tried to roll out customer-facing agents and have run into a whole host of issues getting them into production.

Is it because the technology is limited? Or is it because I have not figured out the best practices to follow to implement this in an optimal way?

I think as we near the ‘Plateau of Productivity’ the industry will start figuring out the ‘optimal way’ to leverage this technology going forward.

In this blog, I wanted to share **where I am deriving the most value from Generative AI** and the use cases we have been working on.

## 🏔️ The Generative AI Value Pyramid

Databricks has a great visual to articulate the value pyramid for generative AI:

[![Generative AI Value Pyramid](/blog/assets/images/blog_images/where-im-getting-the-most-value-from-generative-ai-today-batch-inference-at-scale/generative_ai_value_pyramid.png)](/blog/assets/images/blog_images/where-i’m-getting-the-most-value-from-generative-ai-today-batch-inference-at-scale/generative_ai_value_pyramid.png)

Many teams (and I am totally guilty of this too!), start by building fancy UI’s and chatbots first to start leveraging generative AI.

I have made the joke in the past to friends and fellow colleagues that if I have to build one more chatbot, I may go crazy 🤪.

You will notice in the pyramid visual above, Databricks mentions that **‘batch inference delivers real value, fast!’**

But what is batch inference?

---

## 🤷‍♂️ What is Batch Inference?

**Batch inference** is when you run an AI (LLM) or machine learning model on a large set of data all at once instead of processing it piece by piece. This usually happens on a schedule, like a nightly job, using automated workflows or pipelines. The model processes the data, and the results, such as predictions, categories, or summaries, are saved back into a data system where they can be used for reports, applications, or decision making.

In practice, this means you’re enhancing your existing ETL or data engineering pipelines by adding AI as another transformation step. So instead of just cleaning, joining, and reshaping data, you can now enrich it with intelligence, like classifying documents, detecting anomalies, or generating insights at scale.

---

## 🧱 How Does Batch Inference Work in Databricks?

Databricks has the concept of [**AI Functions**](https://learn.microsoft.com/en-us/azure/databricks/large-language-models/ai-functions), and AI Functions allow you to *‘apply AI, like text translation or sentiment analysis, on your data that is stored on Databricks’*.

The cool part here is that these functions are invokable via code and are easily integrated into your pipelines.

We will talk about some of the use cases I am seeing below, but let’s talk about concepts a bit more to make sure we have a good understanding of how they work.

Databricks exposes a number of [**task-specific AI functions**](https://learn.microsoft.com/en-us/azure/databricks/large-language-models/ai-functions#-task-specific-ai-functions), that can do a variety of things like analyze sentiment, classify input text according to labels you provide, amongst other things.

There is also a function called `ai_query()` which enables you to invoke models hosted in the [**Mosaic Model Serving**](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/model-serving/) platform. It basically calls LLM or ML models via their REST API's.

This is incredibly powerful and we have used this to invoke foundational models, custom agents, and agents created via [Agent Bricks](https://learn.microsoft.com/en-us/azure/databricks/generative-ai/agent-bricks/).

Let's talk about a few use cases we are working on to cement these concepts.

---

## 🤖 Use Cases

There are a few use cases we are working on, some are in production, while others are still in development.

### 🏷️ Classification

We are pulling incidents out of our **EAM (Enterprise Asset Management System)** into our Lakehouse. Inside the incidents table is a free text description field where operators in the Permian Basin manually record details whenever an incident occurs. These incidents can range from minor events, like a worker tripping on site, to more serious safety or equipment issues.

We applied the `ai_classify()` function to that free text description field to enable an LLM to categorize it. Our SQL function looked similar to the example below:

```sql
SELECT
    description,
    ai_classify(
        description,
        ARRAY(
            'personal safety',
            'equipment/mechanical failure',
            'process/operational upset',
            'environmental',
            'vehicle/transportation',
            'fire/explosion',
            'regulatory/compliance'
        )
    ) AS category
FROM
    incidents
LIMIT 10;
```

We then created a new column called `ai_generated_category` and worked with the end users to define what 'good' looked like.

This data was presented in a PowerBI report and provided efficiency gains when generating reports on incident trends at our facilities.

### 📝 Summarization

Plains Midstream is going through a [**large divestiture**](https://finance.yahoo.com/news/plains-american-paa-flexibility-enhances-055251476.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAMq-JoCc5nl--zx8H9wyAV7ekDI1Sge5rwu3yPOPeQhrH2wcAdxHo86WEafhylYGCQUJVEBJWVr3qOLFuMdw6mfo-4yfy1NKy2KHxLDTtEJbY4UUoNaX6yS2FQFeFt0tpmbQeam3ku1aVkFaD-8XwEiP8_V9xGXviX7POdI4-eip) effort right now and there is a lot of data that needs to be analyzed in an incredibly short window of time.

Amongst other things, contracts dating back to the 80’s must be reviewed and bucketed into categories of *‘review’*, *‘divest’*, or *'retain’*.

There are several data points that need to be evaluated to make an informed choice as to what bucket to put that contract into.

For example:

- Does that contract contain a sold or retained asset?
- What legal entity is mentioned in the contract?
- Are there any clauses like right of first refusal or change of control defined in the contract?

To help with the analysis and indexing of **20,000+ contracts**, we decided to leverage Agent Bricks [**Custom LLM**](https://learn.microsoft.com/en-us/azure/databricks/generative-ai/agent-bricks/custom-llm#model-specialization) agent.

Leveraging that agent allows us to guide it by specifying fields like:

- *‘Identify ROFR Clause if it exists. Make sure to identify the section where it exists.’*
- *‘Identify if any sold assets are mentioned. Leverage the list below to identify the sold assets:’*
- *‘Identify legal entity if it exists. Make sure to identify the section where it exists.’*

Once the agent is created, we can invoke this 'at scale' across all **20,000+ contracts** via a SQL statement like so:

```sql
SELECT
  file_name,
  ocr_text,
  ai_query(
    't2t-1234-endpoint',
    ocr_text,
    failOnError => false
  ).result AS ai_summary
FROM catalog.schema.table
```

This enables us to expose a summary of the contract so the lawyers can easily glance at the salient information for the divestiture.

We then leveraged Databricks Apps to create a custom front-end application where the lawyers could select the original PDF and contrast it with the AI-generated summary to ensure we are providing the source file that the LLM used to generate the summary.

### 🧩 Structuring Data

The last use case I want to talk about is adding structure to unstructured data. We leverage the [AI extract function](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_extract) called `ai_extract()`. Providing OCR’d text to this function lets you extract structured fields from it.

We parsed this structured data downstream, wrote it to a delta table, and then set up a [Genie Space](https://learn.microsoft.com/en-us/azure/databricks/genie/) where an LLM can write SQL queries for you based on natural language input.

---

## 🥳 Conclusion

Generative AI is still evolving, and while the hype is real, the most tangible value I’ve seen so far comes from integrating AI into existing data workflows, especially through batch inference. Whether it’s classifying incidents, summarizing contracts, or structuring messy data, the impact is clear when AI is applied thoughtfully and with the end user in mind. There’s still plenty to learn, but focusing on practical use cases is where the real progress happens.

Thanks for reading! 😀
