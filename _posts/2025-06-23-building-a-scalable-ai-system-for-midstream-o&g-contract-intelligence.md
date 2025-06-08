---
title: "🤖🛢️ Building a Scalable AI System for Midstream O&G Contract Intelligence"
date: 2025-06-23T10:00:00-04:00
categories:
  - Data
tags:
  - LLMs
  - GenAI
  - Data Engineering
  - Oil & Gas
---

{% raw %}<img src="/blog/assets/images/blog_images/building-a-scalable-ai-system-for-midstream-o&g-contract-intelligence/blog_image.png" alt="">{% endraw %}

## 🚀 Introduction

The midstream oil and gas industry is burdened by complex contracts that are often lengthy, unstructured, and scattered across various formats. These contracts, which govern everything from transportation and storage to marketing of crude oil and natural gas, pose significant challenges in data accessibility, analysis, and management. With vast amounts of unstructured data, the ability to quickly search, analyze, and ensure compliance becomes critical.

In this post, I'll walk you through a real-world use case where we leverage data engineering and Generative AI (GenAI) to transform contract management in the midstream sector, turning these data challenges into opportunities for greater efficiency and accuracy.

---

## 📃 Problems Plaguing Midstream Oil and Gas Companies

Midstream oil and gas companies encounter several issues with their contracts:

- **Unstructured Data**: Contracts for storage, transport, and marketing are often lengthy and filled with unstructured data that is difficult to navigate and interpret manually.
- **Inconsistent Formats**: Many contracts come in various formats, lacking standardization, which complicates data extraction and analysis.
- **Time-Consuming Processes**: Manual searches through piles of documents to find specific information are time-consuming and prone to errors.
- **Regulatory Compliance**: Ensuring compliance with Federal Energy Regulatory Commission (FERC) parameters and other regulatory requirements through manual review is challenging.

**With many of these contracts being difficult to search and query, this can open up companies to varying degrees of risk.**

There are also scenarios of contracts not being centralized in one location or being stored in SMB file shares on premise which often turn into dumping grounds for files.

This presents challenges from a data quality perspective and the data set may not contain and exhaustive set of contracts or it may not be a curated library and could contain files/contracts that are not relevant.

Making sure you understand these potential challenges or limitations from the get-go is critical to ensure a successful product is rolled out for your business. As someone wise once told me, **‘never use data that you don’t understand the quality of’**.

From my experience, I think centralizing contracts in a SharePoint site is great since it enables teams to leverage ['contract management'](https://support.microsoft.com/en-us/office/use-the-contracts-management-team-site-template-powered-by-microsoft-syntex-80820115-c700-4a62-bb59-69b33c8e3b4f) functionality and even opens the door to some citizen development to leverage tools like [Syntex](https://learn.microsoft.com/en-us/microsoft-365/syntex/syntex-overview) to tag your contracts with metadata.

My point is, the solutions you build as a data engineer will only be as good as the data you use to build it. Data quality is very important. AI is not a magic bullet.

---

## 1️⃣ The First Approach

Let’s dive into some of the technical details behind our initial strategy to address the challenges outlined earlier.

In contract management, data engineering and Generative AI (GenAI) offer a powerful way to transform unstructured documents into structured, searchable formats—enabling faster access, analysis, and decision-making.

Since midstream contracts are typically lengthy, inconsistent, and written in natural language, they're difficult to parse, query, or analyze with traditional methods. Our initial approach focused on extracting predefined structured fields from these documents using OpenAI’s [structured output parser](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/structured-outputs?tabs=python-secure%2Cdotnet-entra-id&pivots=programming-language-python).

The idea was straightforward:

- Subject matter experts provided a list of ~10 fields they needed from each contract.
- We passed each document through an LLM pipeline and extracted these fields.
- The results were visualized in Power BI for downstream filtering and analysis.

At first, this worked well. But over time, we encountered some real-world limitations.

After a few months of usage, additional field requirements emerged. The team came back asking for two more fields to be extracted—not just going forward, but also **retroactively from all previously processed contracts**.

This prompted a few critical questions:

- 🔁 **Reprocessing**: Is it scalable (or affordable) to reprocess every contract each time the field list changes?
- 🎯 **Accuracy**: How do we maintain consistent output quality for the original fields when expanding the schema?
- ⚠️ **Governance**: How do we validate that past extractions didn’t regress with the updated prompt logic?

These challenges exposed some scalability risks with this tightly coupled, prompt-based approach. While it worked well for early experimentation, we realized a more flexible, modular strategy was needed to support ongoing field evolution and robust analytics.

This led us to rethink the system architecture and explore a more composable, search-friendly, and intelligent solution.

---

## 2️⃣ The Revised Approach

In most of our cases, the various personas across the business would ‘search’ for this data in a well defined way. In the example of crude oil marketing, they deal with something called FERC indexing parameters.

### 🔍 What is FERC Indexing?

FERC indexing refers to a pricing mechanism used in the U.S. midstream oil and gas sector to adjust pipeline tariffs, like transportation rates—on an annual basis. These adjustments are designed to account for inflation and changes in operating costs.

Here’s a quick breakdown:

- **FERC** stands for the *Federal Energy Regulatory Commission*.
- FERC regulates interstate oil pipeline transportation rates in the United States.
- Instead of requiring pipelines to submit detailed cost-of-service filings each year, FERC allows many of them to adjust tariffs using an industry-wide **indexing system**.

This index is typically tied to the **Producer Price Index (PPI)**, with an added adjustment factor determined by FERC. While the index itself is updated **annually**, the adjustment formula is **re-evaluated every five years**.

FERC indexing plays a key role in how crude oil marketing contracts are negotiated and interpreted, which is why being able to quickly identify and analyze these parameters across hundreds of contracts is so valuable.

### 🤿 Solution Deep-Dive

Given all the challenges mentioned above and with FERC parameters always changing, trying to do this over hundreds of contracts with many different counterparties, pipelines, terminals, and crude grades can quickly become overwhelming.

Our revised approach focused on designing an intelligent contract analysis system using a combination of data engineering, vector search, agentic orchestration, and Retrieval-Augmented Generation (RAG).

Here’s how we tackled it:

#### 🧠 Step 1: Extract Primary Filtering Fields

We started by identifying and extracting **core structured fields** that users most commonly filter on. These included:

- Counterparty name  
- Contract number  
- Whether the contract contains FERC language

These fields were chosen based on patterns observed in user behavior and repeated requests from analysts. Essentially, we asked: *What do people always need to know to triage a contract?*

We used **PySpark** and **LLM-based extractors** to generate this structured metadata and stored it in a curated table in Unity Catalog. This made it queryable via **Spark SQL** or PowerBI for baseline analytics.

#### 🔍 Step 2: Enable Natural Language & Semantic Search

To allow users to go beyond simple filtering and **ask natural questions** like:

> "Show me all contracts from 2022 that include a 3% FERC escalation"

...we needed something more 'built for purpose' than SQL.

We used **Databricks Vector Search** to index the contracts semantically, embedding the text so we could retrieve **the most relevant chunks** based on user questions. This enables similarity search over contract content, allowing users to surface *concepts*, not just keywords.

#### 🤖 Step 3: Build a Multi-Step Agent Flow

To guide the analyst through the process, we built a **LangGraph-based agentic workflow** that:

1. Accepts a natural language question from the analyst.
2. Filters the results using Spark SQL + metadata filters for precision (e.g., counterparty).
3. Uses the vector search index to find the top-k relevant contract snippets.
4. Presents a summary or exact text excerpt.

This agent acts like a **guided copilot**, progressively narrowing down from the full contract universe to a filtered, relevant dataset based on both structured metadata and unstructured language embeddings.

We also built in **tool awareness** (i.e., the agent knows when to call vector search vs. SQL vs. LLM summarization), and allowed analysts to **pivot back to structured views** (e.g., “show me a table of all matches”) or drill into the raw documents.

#### 🔁 Step 4: RAG Over a Focused Set

The final step in the analyst’s journey is applying **Retrieval-Augmented Generation (RAG)** on the subset of contracts returned by the filtering + search process. This is where users can ask specific questions like:

> “What does this contract say about termination clauses?”  
> “What are the key milestones detailed in this contract?”  
> “What’s the renewal process?”
> "What's the total contract value?"

Since the agent has already narrowed down the scope to relevant documents, the RAG component becomes more accurate and targeted, **avoiding hallucinations** and irrelevant answers.

---

## ✅ Benefits for Midstream Companies

This modular, composable system—leveraging structured extraction, semantic search, and agentic reasoning enables analysts to go from **hundreds of contracts to actionable insights in minutes**.

By combining **LLM flexibility** with **enterprise-grade data engineering** and **governed compute environments**, we delivered a solution that is scalable, traceable, and extensible across use cases.

The integration of data engineering and GenAI brings numerous benefits to midstream oil and gas companies:

- 💼 **Compliance**: Simplifies adherence to FERC and regulatory standards through structured and traceable data.
- 💡 **Insight Generation**: Improves contract visibility and supports strategic decisions.
- ⏱️ **Efficiency**: Automates contract parsing, reducing manual effort and time.
- 💰 **Cost Reduction**: Minimizes human error and contract-related overhead.

---

### 📌 Conclusion

Midstream oil and gas companies face a mountain of unstructured contract data, but with the right blend of AI and engineering, that challenge becomes a strategic advantage. By starting with clean, centralized data and layering on intelligent systems—like vector search, metadata filtering, and RAG, you enable faster decisions, stronger compliance, and a more scalable future.

This isn’t just a technology story, it’s about giving teams the tools they need to unlock value hidden in their documents. And as regulations evolve and data volumes grow, having this kind of system in place will only become more important.

Thanks for reading! 😀

🚀 If you're tackling similar problems in the energy space or beyond, I'd love to hear from you.
