---
title: "Midstream Commercial Optimization with S&P Global Energy Data"
date: 2026-10-22T10:00:00-04:00
categories:
  - Energy
tags:
  - Databricks
  - S&P Global Energy
  - Midstream
---

{% raw %}<img src="/blog/assets/images/blog_images/midstream-commercial-optimization-with-spge-data/blog_image.jpeg" alt="">{% endraw %}

Last week I had the opportunity to co-present with [Hayden Fiege](https://www.linkedin.com/in/hayden-fiege/) and [Nathaniel Ewest](https://www.linkedin.com/in/nathaniel-e/) at the Energy Forum here in Calgary.

Thank you to all those who came out for the event. We had a great turnout. I wanted to include the video recording of the demo we gave, to show the power of blending your internal data with the S&P Global Energy datasets. I have also included some text to describe it if you prefer.

<video controls playsinline preload="metadata" width="100%">
  <source src="/blog/assets/images/blog_images/midstream-commercial-optimization-with-spge-data/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

While I put together this demo, I thought a lot about a blind spot I ran into during my years working in midstream.

You know your own assets really well. Contracts, throughput, and plant performance all sit in your systems, and you can slice them a hundred different ways. The problem is everything happening **outside your fence line**:

- Who is drilling next to your plant?
- Who just bought land?
- Who is about to build a competing facility down the road?

In this post, I wanted to share a demo I built that tries to answer those questions by bringing internal operations data together with S&P Global's industry datasets on Databricks.

> **Note:** Northgate Midstream is a fictional company. I made it up. The plants, contracts, and shippers are synthetic. The S&P data around it is real: real wells, real competitor plants, and real land sales. The workflows are ones I've watched commercial teams struggle with during my time in midstream O&G.

---

## What is S&P Global bringing to the table?

The demo focuses on 2 S&P Global datasets.

### Canada Upstream Content

[Canada Upstream Content](https://www.marketplace.spglobal.com/en/datasets/canada-upstream-content-(1726090820)) is well-level data: production history for every well, plus Crown land and land sale history. Coverage goes back to 1949, and it is updated daily.

For this demo I used 2 pieces of it:

- Monthly production for the Montney wells around Northgate's plants
- Alberta land leases issued since late 2024

### Midstream Essentials

[Midstream Essentials](https://www.marketplace.spglobal.com/en/datasets/midstream-essentials-energy-infrastructure-database-(1682528732)) is S&P's energy infrastructure database. It covers over **4.4 million kilometres** of pipelines and **150,000 facilities** worldwide.

I used 2 pieces of this one too:

- Gas processing plants
- Compressor stations

That's how we see who else is operating, or planning to build, around Northgate.

Think of it this way:

- Your **internal data** tells you what is flowing through your plants.
- **S&P** tells you what is happening in the neighbourhood.

Put them side by side and you start to see things you couldn't before.

---

## Meet Northgate Midstream

To show what you can do with that combination, I created a fictional midstream company called **Northgate Midstream**. Prior to joining Databricks, I spent just about 3 years at a midstream company based in the US, so I hope this is a representative example.

Northgate is a mid-size Montney gatherer and processor around Grande Prairie. They run **3 gas plants** with about **800 MMcf/d** of combined capacity. With LNG Canada shipping since mid-2025 and the Montney now close to half of Canada's gas, every plant up there is competing for the next molecule.

| Plant | Role | Capacity | In service |
|---|---|---|---|
| **Elmworth** | Deep cut, the big one | 350 MMcf/d | 2016 |
| **Karr** | Sour plant | 250 MMcf/d | 2019 |
| **Valhalla** | The new one | 200 MMcf/d | 2021 |

Behind that there is about **320 kilometres** of pipe, **12 compressor stations**, and **36 contracts** with **14 producers**, ranging from a couple of seniors down to a handful of juniors. All in, it is about **$295 million** a year in fees.

So for the demo, pretend you are on Northgate's commercial team. You have all the internal data: contracts, throughput, and plant performance. What you don't have is a good view of what is going on outside your fence. That is the gap those 2 S&P datasets fill.

Put the two together and each plant gets a pretty clear job:

- **Defend** Elmworth
- **Watch** Karr
- **Grow** Valhalla

I broke the demo into 3 workflows to show what that looks like in practice. Let's start with growth.

---

## Workflow 1: Growing Market Share

Valhalla is running at only **54%**. That's roughly **90 MMcf/d** of capacity Northgate has already paid for, sitting there empty. Internal data tells you the plant is underutilised. It doesn't tell you where the gas could come from.

On the S&P side, the map shows:

- Blue hexagons for real Montney wells, coloured by gas rate
- Purple parcels for land sales since late 2024

Once you layer that in, the picture changes quickly:

| Signal | What it shows |
|---|---|
| Nearby production | Up about **30%** in under 2 years |
| Land prices near Valhalla | Around **$1,950/hectare** this year |
| Land prices near Elmworth | About **1/5** of Valhalla's rate |

The area is growing, people are paying up to get in, and the plant is half empty. Northgate's share is actually slipping. You can't see that in either dataset on its own. You need Northgate's receipts divided by S&P's production.

It gets specific pretty quickly too. Click a cluster and it shows who is producing there, and whether they are already in the BD pipeline.

The **Grow** view surfaces the producers Northgate is chasing. Every one of them comes from the S&P production data, with wells within about **40 kilometres** of the plants. I masked the names for the demo.

I've already ticked the **3 third-party deals** targeting Valhalla. That's about **32 MMcf/d**. It moves Valhalla from **54% to around 71%** and adds about **$14 million** a year in fees. Call it **$6 million** once you weight it for win probability.

My favourite part is a little badge that says **self-processes**. S&P tells us those operators already own plants nearby. That's the deal your BD team probably shouldn't spend 6 months chasing.

---

## Workflow 2: Defending Existing Revenue

Growth is the fun part, but hanging on to what you already have pays the bills.

**$126 million** a year of Northgate's fees comes up for renewal in the next 2 years. **$95 million** of that is high risk.

Take the top row, **Muskeg Hollow**. Internally, the numbers already look shaky:

- They're delivering only **61%** of their volume against an **80% take-or-pay** minimum.
- The contract is up in about **6 weeks**.

If that's all you look at, you send a shortfall invoice.

Now add S&P. There is a **280 MMcf/d** plant proposed just **4.6 kilometres** from Elmworth. Whether it ever gets built or not, that is the leverage the customer is bringing to the renewal conversation.

Put those together and the shortfall invoice is the least of Northgate's worries. This is a customer who might already have one foot out the door, and a **$17 million** a year contract the commercial team needs to go win back this month.

Elmworth is carrying about **$96 million** of that renewal risk. If I were on this commercial team, that's where I'd be spending my quarter.

---

## Workflow 3: Just Ask Northgate

Not everyone wants to live in a dashboard, and honestly I get it. For those folks, I built a chatbot called **Ask Northgate**.

Anyone on the team can type a question in plain English and get an answer back. I picked this one on purpose, because it needs both datasets: Northgate's contract terms and S&P's competitor plants.

> Which contracts expiring in the next 12 months are high renewal risk, and who is the nearest competitor?

It works off the same governed tables in Unity Catalog. It writes the SQL, runs it, and hands back the answer, the table, and the exact SQL it ran. Nothing hidden. Someone on the commercial team can get what they need themselves instead of waiting on an analyst to build a report.

## Conclusion

The hard commercial questions in midstream rarely have answers sitting in one system:

- Your **internal data** tells you how you're performing.
- **External data** tells you what is coming at you from outside the fence.

There's plenty more I want to try with these datasets, but starting from practical commercial questions like these feels like the right place to begin.

If you're working on something similar, I'd love to hear from you.

Thanks for reading 😀
