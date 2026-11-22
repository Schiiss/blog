---
title: "Industrial AI: Turning Engineering Data into Decisions"
date: 2026-11-20T10:00:00-06:00
categories:
  - Energy
tags:
  - Databricks
  - Oil & Gas
  - Data Engineering
  - Data Quality
  - GenAI
  - Industrial AI
---

{% raw %}<img src="/blog/assets/images/blog_images/industrial-ai-turning-engineering-data-into-decesions/blog_image.png" alt="">{% endraw %}

Building AI on top of industrial data is hard enough. Building it on data you don't really understand is a lot harder.

I recently gave a talk hosted by APEGA called Industrial AI, Turning Engineering Data into Decisions, and I wanted to write up what we covered for anyone who couldn't make it (or anyone who did and wants it in a format they can skim later).

Huge thanks to [Farheen Akbar](https://www.linkedin.com/in/farheenakbar/) for having me out to speak.

> Note: There is an AI component to this post, but AI is not really the focus. AI gets most of the attention when it comes to engineering data, and I think a lot of the important work that sits underneath it gets missed. That's the stuff I wanted to spend time on.

## A Quote From Mark

I opened the talk with a quote from one of my mentors, [Mark van der Linden](https://www.linkedin.com/in/mark-van-der-linden-30798811/).

"Never use data unless you understand its quality."

Mark has been saying this for about 30 years. He calls himself seasoned. I like to call him old (sorry Mark, I could not resist!).

I think a lot of teams skip right past this, because there is a lot of glitz and glamour around large language models and AI. The unglamorous part is understanding the data and that often gets left behind.

To be clear, this does not mean stopping every project until your data is 100% clean. If we did that, none of us would make it very far. It means understanding the limits of your data, so when you build an AI system (or even a basic report) on top of it, you can set expectations with your end users and nobody takes its recommendations blindly.

## Why Industrial AI Projects Stall Before the AI Starts

A lot of people are excited about the promise of AI. But before most projects ever get to the fun part, there's a lot to work through.

When I think about what makes the move from experimentation to production so hard, I think it boils down to 3 things.

### Data quality is poorly understood

Teams scope AI deliverables before they understand their data.

Take time series sensor data coming out of a historian. From time to time, a sensor might report a null record (a reading with no value) because of network issues or whatever else is going on in the field. You do not want to hand that record to a machine learning model and ask it to decide whether a pipeline is down or leaking.

### Data engineering effort is underestimated

For anyone not familiar with data engineering, the job is to pull data from different places, transform it, and land it somewhere that data scientists, ML engineers, analysts and report builders can actually use it.

With engineering data (time series, unstructured work orders, documents, incident reports, you name it), the initial effort to get this off the ground is huge. Before you get to reporting, let alone machine learning or building agents, someone has to get that data in reliably and in a way people trust.

### Change management gets missed

Operators and engineers have done things a certain way for 10 or 20 years. So why would they change?

Even if you build something great, adoption may never show up if the people using it weren't trained properly or brought along through a real change management process.

I think the idea is to shift from "what AI can we build?" to "what data can we actually trust?"

When you go in with that mindset, the use cases you deliver end up a lot more reliable, because you actually understand the data behind them.

## Where Industrial Data Actually Lives

Engineering data is spread across a lot of different systems, and most of them are siloed. They aren't aware of each other and they don't integrate with each other, so building context across them is hard.

| System | Captures | Where the gap lives |
| --- | --- | --- |
| PLCs / Devices | Raw signals, control actions | No business or asset context |
| SCADA / HMI | Real-time supervision, alarms | Short retention, built for operators |
| Historian | Long-term time series | Tags without consistent hierarchy |
| MES / CMMS | Work orders, failures, downtime | Free-text notes, inconsistent codes |
| ERP | Cost, materials, contracts | Disconnected from physical assets |
| Documents | P&IDs, manuals, inspections | Locked in static PDFs and scans |

Here's the example I carried through the presentation. Your SCADA system (which eventually feeds your historian) shows a temperature or pressure sensor reporting something that looks anomalous. It might be a real problem.

But if you pulled the work orders, you might see an operator just serviced that asset, and the "anomaly" is the asset coming back online. You'd never know that from the historian data alone.

Every system captures part of the picture, and the context gets lost in between.

### OT and IT were built for opposite goals

OT optimises for stability. A lot of the systems they maintain on site are safety critical, and if they go down you could lose line of sight into the temperature and pressure data that tells you how your pipelines are running.

IT optimises for change.

The textbook example is a historian running on a Windows machine. IT sees an out-of-date operating system and wants to patch it. But patching means taking the system offline, and sometimes the app doesn't play nicely with the new OS when it comes back up. That's a lot of friction.

If you're the data team trying to pull this data, build a relationship with both groups. They have opposing goals and that's okay, but if you don't understand those goals you're going to butt heads, and getting access to the data you need gets a lot harder.

### What is the Purdue model?

At a high level, the Purdue model is a way to protect the critical SCADA systems, servers and applications that live on site. Without it, someone who breaks into your company's IT network could also reach all of your OT systems.

Traditionally there's a DMZ or an air gap between the two, so devices on the IT network can't easily talk to devices on the OT network.

That's great for security, and it's a real challenge if your job is to bring historian and engineering data into one central spot. A few things make it tough:

- **Security air gaps.** OT networks sit behind strict DMZ firewalls that block direct cloud egress and IT-side querying.
- **Data frequency and streaming strain.** Historians are optimised for disk compression, not real-time streaming. Poll your tags too often and you can put real pressure on the OT system.
- **Proprietary APIs and legacy interfaces.** Getting asset context out often means working through PI AF SDK, PI Web API, OMF or older OPC-DA drivers, usually with custom wrappers.

![Purdue Model](/blog/assets/images/blog_images/industrial-ai-turning-engineering-data-into-decesions/purdue_model.png){: style="display:block; margin:0 auto;" }

The rule of thumb I like is that analytics platforms read, they never control. The goal is secure, read-only OT streaming that doesn't affect plant stability.

## Building a Data Platform AI Can Use

So, imagine we work through all of that. What does it look like?

At a high level, you bring data from your operational systems (SCADA, PLCs, historians) and your IT systems (ERP, maintenance history in something like Maximo) into one central data platform.

![Central Platform 1](/blog/assets/images/blog_images/industrial-ai-turning-engineering-data-into-decesions/central_platform_1.png){: style="display:block; margin:0 auto;" }

Back to our sensor example. Now that the systems that couldn't talk to each other live in one place, you can actually ask whether there was an open work order on that asset when the reading spiked. That breaks the silos and gives you a trusted foundation to build AI on.

### What is a lakehouse?

It's not the lake house you go visit in the summertime. It's not quite as fun.

Old-school data warehouses were really good at tabular, structured data. You could write SQL against massive datasets. They were not so good with unstructured data like PDFs, Word docs, audio or video. That's what data lakes were for.

The lakehouse is the meet in the middle, and the open file formats are a big part of it.

Traditionally you had analysts writing SQL in one tool, and data scientists and ML engineers writing Python in another, often on closed formats that didn't work together. So everyone ended up working on their own copy of the data.

With open formats (Delta Lake, Apache Iceberg, Parquet and friends) sitting in cloud object storage, data engineers, data scientists and analysts can all work off the same copy of the data without shuffling it between tools.

On top of storage, you need a unified governance layer. Some of the data you bring in will be sensitive, so you need something sitting over the storage layer that gives you:

- Fine-grained access control (down to rows and columns)
- A central catalog so people can find what has been brought in
- Lineage so you can see where data came from
- Audit and compliance so you can see who is doing what with it

![Unified Architecture](/blog/assets/images/blog_images/industrial-ai-turning-engineering-data-into-decesions/unified_architecture.png){: style="display:block; margin:0 auto;" }

### Raw, contextualised, decision-ready

This is the progression I think every industrial data platform should be working toward:

- **Raw feed.** Land everything as-is and keep the full history.
- **Contextualised.** Attach units, asset hierarchy and quality flags.
- **Decision-ready.** Aggregated KPIs and verified features for AI.

In practice, a raw sensor like `snsr_vib_1049f` means nothing on its own. Once you map it, you know it's measuring vibration on Pump-B at Pump Station 4, which belongs to a particular plant. Now if it looks anomalous, you have the context to decide whether it's worth investigating.

![Raw to contextualized](/blog/assets/images/blog_images/industrial-ai-turning-engineering-data-into-decesions/raw_to_contextualized.png){: style="display:block; margin:0 auto;" }

### Treat data quality as a first-class engineering concern

Every reading should carry its quality status, the same way a lab result carries its uncertainty. Some of the basic checks I'd start with:

- **Flatline detection** to catch stuck sensors posing as stable operation
- **Rate-of-change checks** to flag physically impossible spikes
- **Timestamp gap checks** to catch missing intervals and late-arriving data

![Data quality](/blog/assets/images/blog_images/industrial-ai-turning-engineering-data-into-decesions/data_quality.png){: style="display:block; margin:0 auto;" }

Most platforms let you write these as simple SQL rules that run as the data comes in. Something like this (illustrative only, your tags and thresholds will be different):

```sql
SELECT
  tag_id,
  ts,
  value,
  CASE
    WHEN value IS NULL THEN 'NULL_READING'
    WHEN value = LAG(value) OVER (PARTITION BY tag_id ORDER BY ts)
     AND value = LAG(value, 2) OVER (PARTITION BY tag_id ORDER BY ts)
     AND value = LAG(value, 3) OVER (PARTITION BY tag_id ORDER BY ts)
      THEN 'FLATLINE'
    WHEN ABS(value - LAG(value) OVER (PARTITION BY tag_id ORDER BY ts)) > 50 THEN 'RATE_OF_CHANGE'
    WHEN ts - LAG(ts) OVER (PARTITION BY tag_id ORDER BY ts) > INTERVAL 5 MINUTES THEN 'TIMESTAMP_GAP'
    ELSE 'OK'
  END AS quality_flag
FROM sensor_readings
```

And again, poor quality is not a reason to sit on your data. I borrowed this analogy from [Chad Wahlquist](https://www.linkedin.com/in/chad-wahlquist/) at Palantir: saying you'll use your data once it's clean is like saying you'll start working out once you're in shape. You get your data in shape by moving it and using it. That's how you learn where to spend your clean-up effort and where you can live with it.

## The energy industry has the data

I come from energy, so I'm going to be a bit selfish here.

There is no shortage of data in this industry. Upstream has well logs. Midstream has take-or-pay and volumetric contracts. Downstream has refineries full of sensors. Whatever industry you're in, I bet you can relate.

What's missing is trust in that data and the context around it. That anomalous reading means nothing until I know when the sensor was serviced, who serviced it, and where it sits in the overall facility.

Where I think we're heading is field sensors and historians feeding a governed data layer, a semantic model on top of that, and AI and agentic applications on top of the semantic model. AI sits on the semantic layer, never on raw tags.

![Energy data](/blog/assets/images/blog_images/industrial-ai-turning-engineering-data-into-decesions/energy_data.png){: style="display:block; margin:0 auto;" }


## The Demo

The demo was built on Databricks, but the concepts apply regardless of platform. We:

1. Extracted and parsed both structured and unstructured data, including P&IDs (piping and instrumentation diagrams), work orders and inspection reports
2. Pulled equipment tags, dates and findings out of those documents into a table
3. Interacted with the context layer we had just built

Here is the demo:

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;"><iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" src="https://www.youtube.com/embed/vhmTgIy7fvw" title="Industrial AI demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

## Where AI Is Working Today

The use case I shared came from my time in midstream oil and gas. We were asked to help avoid unnecessary pipeline shutdowns.

As I understand it, when an alarm fires, the pipeline operator has to decide whether to keep the pipeline running or shut it down.

- **False positive.** The operator shuts down and there's no leak. The line is down for 3 to 4 hours, at roughly $50-100K USD an hour, before you even count commitments to refineries and other customers.
- **False negative.** The operator keeps running because "we get this alert all the time." The pipeline is actually leaking, and now you're dealing with environmental, regulatory and public perception issues.

Alarm fatigue is a thing. When operators are buried in noise, the critical alert is the one that gets ignored.

Here's roughly what we built:

1. Worked with the OT team to identify which sensors in our AVEVA PI historian actually mattered for understanding pipeline state
2. Brought in PODS (the Pipeline Open Data Standard) so we could visualise pipelines geospatially on a map
3. Brought in work orders, so we knew when a pump or a section of pipe was being serviced
4. Ran the data engineering pipelines 24/7, since a lot of our pipelines were running at capacity and always producing sensor data
5. Fed that high-quality, well-understood data to a machine learning model that predicted which of 4 states the pipeline was in (running normal, shutting down, shut down, or anomalous)
6. Exposed the results in reports and sent real-time alerts when something was detected

The piece we started experimenting with toward the end was an AI agent. It had no chat interface. As soon as an alarm fired, the agent went looking for open work orders, what was happening upstream, and what had changed since the anomaly was triggered.

It did not replace the operator by any means. It gave them a head start on where the issue might be.

## Looking Ahead, The Next 3 Years

There's no doubt there's a lot of power in large language models and AI agents. And a lot of companies are already pulling their enterprise data into central platforms.

Where I think most of the next 3 years gets spent is the middle layer, what we call the context layer. Unified metadata, asset hierarchies, semantic models and the relationships between them, sitting between your enterprise systems (CMMS, SCADA, time series, PDFs, contracts) and the LLMs and agents on top.

It ties right back to the sensor example. A single reading doesn't mean much to me without the surrounding context, and the same goes for an LLM.

The argument we make at Databricks is that these models are more than capable at this point. They're usually just missing access to the right data, and the context layer is how you give it to them. Grounding an agent in that layer is also how you keep it from making things up about your plant.

![Looking ahead](/blog/assets/images/blog_images/industrial-ai-turning-engineering-data-into-decesions/looking_ahead.png){: style="display:block; margin:0 auto;" }

## A Practical Framework for AI Readiness

I wrapped up with a few questions worth asking yourself before you start building.

| Pillar | Ask yourself | Ready looks like |
| --- | --- | --- |
| Trust | Do we measure data quality? | Quality flags on every critical tag |
| Context | Can a new hire interpret a tag? | Asset hierarchy and units attached |
| Access | Can teams reach data without CSVs? | One governed place to query |
| Ownership | Does every dataset have an owner? | Documented rules and lineage |
| Use case | Is there a specific decision to improve? | Measurable baseline before modelling |

A couple of notes on these.

On context, a tag by itself means nothing. What are you relating it to, and what are you adding so someone new can actually read it?

On ownership, I've rarely seen this done well. Lots of companies have governance programs that try to name data owners, and you want those owners deciding things like sensitivity classification (does this need to be locked down to certain groups, or can everyone see it?). It's hard to execute, but it's a big part of any governance strategy.

On use case, make sure there's a specific decision you're trying to improve, and that you can measure it before you start modelling. In [a podcast](https://youtu.be/MudEaQZfefE), [Wish Bakshi](https://www.linkedin.com/in/wishbakshi/) described how creativity used to be abundant while execution was scarce. With LLMs, creativity is still abundant, and execution is now abundant too, so be thoughtful about what you build.

## Wrapping Up

AI is genuinely exciting. But I really think the companies that get the most out of it will be the ones putting the work into data quality and the context layer first.

There's still plenty for me to learn here, and I'd love to hear from you, good feedback and bad.

Thanks for reading!