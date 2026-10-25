---
title: "Databricks Genie App Builder and S&P Global Energy Data"
date: 2026-10-22T10:00:00-04:00
categories:
  - Energy
tags:
  - Databricks
  - Genie
  - Genie App Builder
  - Vibe Coding
---

{% raw %}<img src="/blog/assets/images/blog_images/databricks-genie-app-builder-and-s&p-global-energy-data/blog_image.jpeg" alt="">{% endraw %}

Having worked in the energy sector for a few years I have learnt that oil and gas companies are sitting on a wealth of data. Data teams put a ton of effort into identifying, extracting, and transforming data into their tool of choice for downstream analytics, data science, report building and so much more.

A lot of that effort goes into third-party data. Production numbers, pricing, risk scores. Someone has to pull it in, clean it up, and keep the pipelines alive before anyone gets to ask a single question of it.

At Databricks, we have been working closely with [S&P Global](https://www.marketplace.spglobal.com/en/), specifically its S&P Global Energy division, on changing how energy data is distributed and consumed. S&P Global Energy datasets are available to Databricks customers via the Marketplace and are shared through the [OpenSharing protocol](https://docs.databricks.com/aws/en/opensharing/), which effectively removes the "E" from ETL. You get to focus on the downstream use cases instead of the nitty gritty data engineering needed to collect the data.

In addition to talking about the S&P data, I also wanted to take the opportunity to get hands-on with the new [Genie App Builder](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/genie-app-builder), the new Databricks feature for governed agentic app building.

## S&P Datasets

S&P Global Energy publishes many of its datasets via the [Databricks Marketplace](https://marketplace.databricks.com/) (S&P has a [page on its Databricks offering](https://www.marketplace.spglobal.com/en/solutions/databricks-delta-sharing-(6d6034f6-fcc6-40b6-bfbf-3fed9a753ce8)) too). The fact this is shared via the [OpenSharing](https://docs.databricks.com/aws/en/opensharing/) protocol is a huge win for customers in my opinion.

### What is OpenSharing?

If you have not come across OpenSharing before, the idea is pretty simple. The traditional approach is a data provider dumping files into an S3 bucket or an SFTP server, and you building a pipeline to ingest, clean, and load that data into your platform. OpenSharing skips all of that and lets the provider share data directly into your Unity Catalog.

Think of it like this, the data just shows up in your catalog, ready to query. The provider manages the data on their end, you consume it on yours. When S&P publishes an update to their world oil supply numbers, it is available to you without a single line of ETL code running on your side.

I have seen teams at midstream and upstream companies dedicate entire sprints to building and maintaining ingestion pipelines for vendor data. OpenSharing largely removes that overhead.

Getting set up is pretty simple. Once S&P provisions the share to your Unity Catalog metastore (using your metastore's sharing identifier), you navigate to the Catalog explorer, find the share under "Shared with me," and create a catalog from it. A few SQL commands and you are querying S&P data alongside your internal datasets.

```sql
-- List providers sharing with you
SHOW PROVIDERS;

-- List shares from a specific provider
SHOW SHARES IN PROVIDER `<provider_name>`;

-- Create a catalog from the share
CREATE CATALOG spge_data USING SHARE `<provider_name>`.<share_name>;
```

### The Datasets

For this example, I am using the [world oil supply](https://www.marketplace.spglobal.com/en/datasets/world-oil-supply-(1681252686)) and [crude supply risk](https://www.marketplace.spglobal.com/en/datasets/crude-supply-risk-(1696261739)) datasets. One tells you how much oil is coming out of the ground, the other tells you how likely it is that something gets in the way. I will dig into what is inside each one later in the post.

---

## What is Genie App Builder?

[Genie App Builder](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/genie-app-builder) is a Databricks-native tool for building apps with natural language, directly in the Databricks UI. You describe the app you want, it generates a working preview, and you refine it until you are happy and deploy.

Under the hood, Genie App Builder builds apps with [Databricks AppKit](https://developers.databricks.com/docs/appkit/v0), the Databricks framework for data and AI apps. Think of AppKit as a TypeScript SDK with a plugin for each Databricks service your app might need: SQL warehouses, Lakebase, model serving endpoints, Genie spaces, and files in UC Volumes (through its Files plugin). It also handles the plumbing you would otherwise wire up yourself, like caching, telemetry, retries, error handling, and OAuth-based authentication.

If you want to try AppKit on its own, the Databricks CLI will scaffold a project for you:

```bash
databricks apps init
```

You pick the plugins you need from a template selector and it generates a Node.js/Express/React project with everything wired up, ready to deploy to a Databricks App.

I like that AppKit goes further than something like Streamlit. Streamlit is great for quick prototypes and data exploration, but once you need proper routing, role-based workflows, write-back logic, or custom UI components, you hit its limits pretty fast. AppKit gives you a React front end with a Node.js/TypeScript back end, which is closer to what a professional developer would reach for. The trade-off is that it expects some familiarity with Node.js and npm, which not every data team has. With Genie App Builder writing the AppKit code for you, that barrier drops a lot.

---

## App Spaces

Outside of the vibe coding itself, the part I think most customers will be excited about is [App Spaces](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/app-spaces).

An App Space is a governance boundary where admins define who can create and use apps, what permissions those apps have, and which spend policies apply to them. Every day I see customers eager to vibe code, but admins are reluctant to hand over the keys to the kingdom, so to speak. And who can blame them? Letting anyone spin up apps against production data comes with real security and cost risk.

App Spaces let admins group apps together so they all inherit shared identity, scopes, and resources automatically. Platform teams can let more people build and deploy apps inside a governed space instead of hand-holding every app setup themselves. Apps built with Genie App Builder also run on isolated, on-demand serverless compute (a single instance at most) that scales to zero when idle, so you are not paying for an internal tool that sits idle most of the week. And during the Beta, it is all free.

When [creating](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/app-spaces#create-an-app-space) an App Space, you configure user authorization, serverless usage policies, and who is allowed to create apps within the space.

![App spaces config](/blog/assets/images/blog_images/databricks-genie-app-builder-and-s&p-global-energy-data/app_spaces.png){: style="display:block; margin:0 auto;" }

---

## Genie App Builder In Action 🛠️

To test this out, I crafted a [prompt](https://github.com/Schiiss/blog/tree/master/code/databricks-genie-app-builder-and-s&p-global-energy-data/prompt.txt) to have Genie App Builder generate a Strait of Hormuz Chokepoint Risk Dashboard. It is a 3-page app that combines S&P's crude supply risk scores with their world oil production data, focused on the Gulf producers whose seaborne exports normally transit the Strait of Hormuz. The EIA lists seven: Saudi Arabia, the UAE, Kuwait, Qatar, Iraq, Bahrain, and Iran. My prompt also included Oman, which it should not have, since Oman loads its crude at Mina al Fahal on the Gulf of Oman, outside the strait. It is also worth knowing that Saudi Arabia (via the East-West pipeline) and the UAE (via the Habshan-Fujairah pipeline) can route part of their exports around the strait.

The prompt asked for:

- **Risk Overview:** KPI cards showing how much of global crude capacity depends on the Hormuz chokepoint, plus a colour-coded table ranking each country by overall price risk, alongside their geopolitical, political violence, and export risk scores.
- **Risk Trends:** A time-series chart of each country's risk scores over time, with a dropdown to switch between risk dimensions (geopolitical, political violence, export, facility violence, labour unrest).
- **Production Exposure:** A stacked bar chart of monthly crude production by country, with toggles to split by supply type (crude, condensate, NGL) and filter by OPEC membership. Plus a KPI card showing Middle East production as a share of global output.

Basically the kind of screen a trading desk or risk team would want up when headlines start coming out of the Gulf.

The first version looked pretty good. I still needed to validate the numbers, but it was a solid start.

![First version of the app](/blog/assets/images/blog_images/databricks-genie-app-builder-and-s&p-global-energy-data/app_v1.png){: style="display:block; margin:0 auto;" }

Next I wanted to nail the look and feel, so I pasted in a screenshot of a cyberpunk themed website and had Genie adapt my app's theme to match.

![Second version of the app](/blog/assets/images/blog_images/databricks-genie-app-builder-and-s&p-global-energy-data/app_v2.png){: style="display:block; margin:0 auto;" }

You will also notice Genie taking screenshots of the app as it works, so it can check its own output.

![Screenshot of app](/blog/assets/images/blog_images/databricks-genie-app-builder-and-s&p-global-energy-data/screenshot_of_app.png){: style="display:block; margin:0 auto;" }

That screenshot loop is the biggest difference from my experience building apps with Genie Code. I use Genie Code and Genie One as my daily agent tools and reach for Omnigent when the scenario calls for it. Genie Code has come a long way and is great for notebooks, pipelines, and dashboards, but building apps with it has been a struggle for me and for customers I work with:

- **No visual feedback loop.** Genie Code could not see the app it was building. In Omnigent (Claude/Codex) I use the [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) so my agent can click around the running app and test it, which makes the feedback loop way faster. Without that, you end up describing broken UI components in chat or pasting screenshots yourself.
- **Inconsistent deployments.** Getting the app deployed often took a few rounds of "App not available" and "App crashing" errors, with me telling it "the app still is not working" over and over. Sometimes, it could not deploy at all. 
- **Multi-page apps got messy fast.** Linear work like generating data, building a pipeline, and creating a dashboard went fine. Once the app had multiple pages and connections to Lakebase, a Genie Agent, and a dashboard, every fix seemed to break something else. I have even seen it decide to ship a static HTML page with no routing or interactivity instead of connecting to live data.

As I understand it, Genie App Builder renders your app in an [iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe) inside the builder, which is how Genie can see the preview and interact with it. An iframe is an HTML element that loads a separate web page inside the current one. Databricks uses them elsewhere too, for example to [embed a dashboard in an app](https://docs.databricks.com/aws/en/dashboards/share/embedding/basic). Using an iframe does not bypass any of your access controls. Users still sign into their workspace and their access is checked against Unity Catalog before they see any data.

---

## SPGE Data 🛢️

We have all seen plenty of slick vibe coded apps at this point and the wow factor has gone down. The data behind this one is what makes it useful, so here is what each dataset contains.

### World Oil Supply

The world oil supply share gives you monthly volumes by country, rolled up by region. Every row is a country, a month, a supply type, a production type, and a value with its units. The table mixes history with S&P's forecasts, which run out to 2028 (short term, monthly) and 2060 (long term, annual, stored with month = 0). For monthly data, filter `scenario_Term_Name = 'Short Term'`.

| Column | What it holds |
|---|---|
| `country_Name` / `region_Name` | Where the barrels are produced (e.g. Saudi Arabia, Middle East) |
| `year` / `month` | Monthly for short-term rows; long-term rows are annual (month = 0) |
| `supply_Type_Name` | The type of liquid: Crude, Condensate, NGL, Refinery Gain, Ethanol, Biodiesel, GTL, CTL, or Ether |
| `production_Type_Name` | What the value measures: Production, Capacity, Spare Capacity (stored as negative numbers), Maintenance, or Disruptions |
| `production_Element_Name` | The crude grade (e.g. Arab Light, Arab Heavy) |
| `value` / `units` | The production figure and its unit of measure |
| `member_Opec` | Whether the country is an OPEC member |

`production_Type_Name` is the column that matters most. If you sum `value` without filtering to `Production`, you add capacity, spare capacity, maintenance, and disruptions on top of actual output. Saudi crude for June 2025 comes out at 19,154 thousand b/d instead of 9,577.

The supply type split is my favourite part. Crude, condensate, and NGLs (natural gas liquids) get lumped together as "oil" all the time, but they move through different infrastructure and price differently. Having them separated means you are not reverse-engineering someone else's totals. The OPEC flag also lets you answer questions like "how much of this region's supply is OPEC-controlled?" without maintaining your own mapping table.

### Crude Supply Risk

Instead of volumes, the crude supply risk share gives you risk scores for each producing country, broken into specific dimensions and tracked over time with a `scoring_date`.

| Column | What it holds |
|---|---|
| `geopolitical_risk` | Geopolitical risk score |
| `political_violence` | Political violence risk score |
| `export_risk` | Risk to the country's ability to export crude |
| `facility_and_personnel_violence` | Risk of attacks on energy facilities and workers |
| `labor_unrest` | Risk of strikes and labour disruption |
| `overall_country_price_risk` | The overall country price risk score |
| `crude_capacity` | The country's crude production capacity |
| `global_capacity` | The country's crude production capacity as influenced by any industry shock (a per-country figure, not world capacity) |
| `reason_for_adjustments` | Short commentary on why a score was adjusted (sparsely populated) |

The capacity columns sitting right next to the risk scores is a nice touch. You can weight risk by how many barrels are actually exposed, because a high score on a small producer is a very different story from the same score on Saudi Arabia. `reason_for_adjustments` can hint at the answer to the question a trader asks when a number jumps (why?), but don't lean on it too heavily. Only about 3% of rows have text, and it is brief (e.g. "major risk focus").

The production data drives the Production Exposure page, and the risk data drives the Risk Overview and Risk Trends pages.

### What S&P Does For You

If you tried to build this yourself, you would be pulling production numbers from national agencies, OPEC reports, and company filings, all on different schedules, in different units, with different definitions of "crude". Then you would need a team scoring geopolitical risk on a consistent methodology across dozens of countries. That is a lot of work before you ever get to the analysis.

I imagine the official numbers also come with some uncertainty. OPEC members have reasons to report figures that help their quota position, and there have been cases of members producing above their limits. Having an independent estimate built from tanker tracking and shipping data gives you a second opinion when the reported numbers do not pass the sniff test.

S&P has already done the normalisation and scoring, and because it is delivered over OpenSharing, it lands in Unity Catalog ready to join with your own data. Here is the kind of query that sits behind the Risk Overview page:

```sql
WITH current_scores AS (
  SELECT *
  FROM <your_catalog>.supplyrisk.country_scores
  WHERE status = 'Current'
)
SELECT
  country,
  overall_country_price_risk,
  geopolitical_risk,
  export_risk,
  crude_capacity,
  ROUND(100 * crude_capacity / SUM(crude_capacity) OVER (), 1) AS pct_of_scored_capacity
FROM current_scores
QUALIFY country IN ('Iran', 'Iraq', 'Saudi Arabia', 'United Arab Emirates',
                    'Kuwait', 'Qatar')
ORDER BY overall_country_price_risk DESC;
```

The percentage is each country's share of total capacity across all scored countries. The window total has to be computed before the country filter, which is why the filter sits in `QUALIFY` rather than `WHERE`. (Bahrain is left out because it is not in the crude supply risk data, and Oman because its exports load outside the strait.)

One small gotcha: the two datasets name the country column differently (`country` in one, `country_Name` in the other), so check that the country values line up before you join them. As always, never use data you don't understand the quality of 🙂

---

## Conclusion

Genie App Builder excites me. I think it addresses a lot of the concerns platform teams have about people vibe coding, and in turn it will put the right tools in the hands of more people who want to build apps. App Spaces are a big part of that, giving admins the guardrails to say yes.

Pairing these Databricks experiences with S&P Global Energy data gets really interesting for energy companies. In a couple hours, I went from a data share to a working Strait of Hormuz risk dashboard. The next step is joining that S&P data with internal data like production volumes or trading positions.

This is still very much the beginning of the exploration. Genie App Builder is in beta, there are rough edges, and I still need to fully validate the numbers in my app. But the feedback loop is faster than anything I have seen for building apps on Databricks so far, and I am pumped to see where it goes.

Here is the final app I created.

> DISCLAIMER: I spot checked these numbers and they look accurate, but any inaccuracies are more likely down to the join and filter logic in the app (written by Genie and reviewed by me) than the underlying S&P data.

![Final Page 1](/blog/assets/images/blog_images/databricks-genie-app-builder-and-s&p-global-energy-data/final_page1.png){: style="display:block; margin:0 auto;" }

![Final Page 2](/blog/assets/images/blog_images/databricks-genie-app-builder-and-s&p-global-energy-data/final_page2.png){: style="display:block; margin:0 auto;" }

![Final Page 3](/blog/assets/images/blog_images/databricks-genie-app-builder-and-s&p-global-energy-data/final_page3.png){: style="display:block; margin:0 auto;" }

A note on the Production Exposure page: it shows all 13 countries S&P groups under the Middle East region (including Egypt, Turkey, Syria, and Yemen), not just the Hormuz producers, and the 30.2% share KPI is S&P's forecast for December 2028. In the same data, the share is 32.3% in December 2025 and 23.9% for September 2026 in S&P's latest outlook. The Risk Overview screenshot still includes Oman; without it, Hormuz-dependent capacity is 33.8 MMb/d, or 33.8% of scored capacity.

Thanks for reading 😊
