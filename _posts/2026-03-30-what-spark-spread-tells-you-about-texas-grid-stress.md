---
title: "What the Spark Spread Tells Us About Texas Grid Stress"
date: 2026-03-29T10:00:00-04:00
categories:
  - Energy
tags:
  - Databricks
  - MCP
  - Oil & Gas
---

![What the Spark Spread Tells Us About Texas Grid Stress](/blog/assets/images/blog_images/what-spark-spread-tells-you-about-texas-grid-stress/blog_image.png){: style="display:block; margin:0 auto;" }

> Note: All prices and spark spreads shown here are derived from ERCOT HB_NORTH real-time settlement point prices (15-minute intervals), Henry Hub front-month natural gas futures (NG=F), and publicly available weather data, all ingested and modeled in Databricks for this project. Spark spreads are calculated using assumed heat rates (7.0 MMBtu/MWh for CCGT, 10.0 for peakers) and represent fuel-cost margins only, not total plant profitability. Values are based on my processed dataset and may differ from official ERCOT settlements, nodal prices, or plant-specific economics. HB_NORTH broadly represents the Dallas/Fort Worth region.

Over the past few months, I've been intrigued by energy markets, especially since I've been working more with the trading team at Plains on use cases like crude blending. To get a better feel for the data energy traders analyze daily, I pulled in data from [ERCOT](https://www.ercot.com/), the [U.S. Energy Information Administration](https://www.eia.gov/), and other sources into Databricks, focusing on the Texas market. This also gave me a chance to get hands-on with [Lakeflow Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/concepts). While I wasn't the biggest fan of its predecessor, DLT, I've heard the new branding brings significant improvements.

The idea I had to start was to look at these various data sources to analyze how extreme weather events impact gas and power prices.

On January 26, 2026, a cold front pushed into Dallas and temperatures fell to 14°F, nearly 40 degrees below the seasonal average. Over the next three days, something remarkable happened to energy markets:

| Date   | Dallas Temp | Gas Price   | Avg Power Price | CCGT Spark Spread |
|--------|-------------|-------------|-----------------|-------------------|
| Jan 21 | 57°F        | $4.88/MMBtu | $22/MWh         | -$11.69           |
| Jan 26 | 14°F        | $6.80/MMBtu | $168/MWh        | +$119.91          |
| Jan 27 | 22°F        | $6.95/MMBtu | $116/MWh        | +$67.05           |
| Jan 28 | 34°F        | $7.46/MMBtu | $200/MWh        | +$147.67          |
| Jan 29 | 42°F        | $3.92/MMBtu | $27/MWh         | -$0.81            |

Gas prices jumped sharply. Power prices quintupled. And then, the moment temperatures recovered, both collapsed and the spread went negative again within 24 hours.

> **The spark spread captures the core economics in a single number.**

[![Power Price vs CCGT Spark Spread + Dallas Temperature, Jan 20–Feb 5, 2026](/blog/assets/images/blog_images/what-spark-spread-tells-you-about-texas-grid-stress/the_cold_snap.png)](/blog/assets/images/blog_images/what-spark-spread-tells-you-about-texas-grid-stress/the_cold_snap.png){:target="_blank"}

The two charts above tell the same story from different angles. The top chart tracks two lines: average power price (what electricity sold for at the HB_NORTH hub) and the CCGT spark spread (the profit margin for a gas plant generating that electricity). On January 21 both lines are flat and low, a mild day with no stress on the grid. Then the cold front arrives on January 26 and both lines spike sharply upward, the power price climbing to $168/MWh and the spread jumping to $120. They stay elevated through January 28 before collapsing back to near zero on January 29 the moment temperatures recovered.

The bottom chart shows why. Dallas average temperature is plotted across the same date range. The V-shaped dip, bottoming out at 14°F on January 26, is the cold snap. The visual alignment between the temperature dip and the price spike in the top chart is the entire point: weather drove demand, demand drove prices, and prices drove the spread. The mechanism isn't abstract, you can see it happen in real time across two charts stacked on top of each other.

The fact that both lines in the top chart move together matters too. In a summer heat wave, power prices spike but gas prices stay cheap, so the spread explodes far above the power price line. In this winter event, gas prices spiked alongside power prices. Gas infrastructure tightened as heating demand and power generation competed for the same fuel. The spread was still strongly positive, but it was more compressed than a typical August afternoon. That compression is the signature of a winter stress event versus a summer one.

---

## What Is The Spark Spread?

[The spark spread is a common metric for estimating the profitability of natural gas-fired electric generators](https://www.eia.gov/todayinenergy/detail.php?id=9911). The spark spread is the profit margin a gas-fired power plant earns for generating one megawatt-hour of electricity. It answers one question: is it worth burning gas right now? They are calculated with the following equation:

```text
Spark spread ($/MWh) = power price ($/MWh) – [natural gas price ($/mmBtu) × heat rate (mmBtu/MWh)]
```

Heat rate measures how many MMBtu of fuel a power plant must burn to generate 1 MWh of electricity. Lower heat rates mean higher efficiency.

- **CCGT** (combined cycle gas turbine, ~55% efficient): `7.0 MMBtu/MWh` — the workhorses that run most of the day.
- **Peaker** (simple cycle, ~34% efficient): `10.0 MMBtu/MWh` — expensive to run, called only when the grid is stressed.

A positive spread means the plant covers its fuel cost and makes money generating. A negative spread means every megawatt-hour it produces loses money on fuel alone.

On January 28, with power at $200/MWh and gas at $7.46/MMBtu, the CCGT spread was $200 − (7.0 × $7.46) = $147.67. Many gas plants were earning extremely high margins. On January 21, with power at $22 and gas at $4.88, the spread was $22 − (7.0 × $4.88) = -$11.69. Few plants would choose to run purely for energy revenue.

This is the same plant, same fuel, five days apart.

---

## Two Types of Grid Stress (And They Look Completely Different)

The Texas grid experiences stress in two different ways and the spark spread behaves differently in each.

### Summer Heat Waves: When Gas Plants Win

August is often the best month to own a gas plant in Texas. August has the highest average CCGT spread at $25.76, making it the most profitable month to own a gas plant in Texas. The next highest months are May ($24.88) and January ($13.46), but August stands out as the clear leader. Temperatures regularly exceed 100°F, air conditioning load pushes demand to annual peaks, and gas prices stay low in summer because heating demand is absent. As a result, power prices spike while fuel costs stay cheap.

On August 20, 2024, the average power price at HB_NORTH hit $226/MWh with gas at $2.20/MMBtu. The CCGT spread that day was $210/MWh. The maximum interval price hit $4,853/MWh. In the entire month of August 2024, there was not a single day with a negative spark spread in my dataset, and according to the dataset I generated, CCGT plants were profitable 86% of all 15-minute intervals.

### Shoulder Season: When Gas Plants Lose Money Every Day

Flip the calendar to late February or early March and the picture reverses completely. Temperatures are mild, demand is low, but gas prices remain elevated from winter. The spread collapses.

These are what we call the dead days, when the spread is so negative that not a single 15-minute interval is profitable:

| Date | Avg Power | Gas Price | CCGT Spread | % of Day Profitable |
|------|-----------|-----------|-------------|---------------------|
| Feb 26, 2025 | $8.64 | $3.91 | -$18.70 | 0% |
| Nov 28, 2025 (Thanksgiving) | $17.53 | $4.85 | -$16.42 | 0% |
| Nov 11, 2025 | $15.17 | $4.57 | -$16.79 | 6% |
| Jan 2, 2026 | $10.92 | $3.62 | -$14.41 | 0% |

On February 26, 2025, not one 15-minute interval across the entire day covered a CCGT plant's fuel cost.

---

## The Seasonal Calendar

The following statistics are calculated from my dataset covering Dec 2023–Mar 2026.

Zoom out, and the pattern holds true year over year. The table below shows multi-year averages at HB_NORTH (Dec 2023–Mar 2026):

| Month | Avg CCGT Spread | % of Day Profitable | Negative Spread Days |
|-------|-----------------|---------------------|----------------------|
| August | $19.82 | 86% | 0 |
| May | $18.58 | 53% | 9 |
| March | $1.15 | 42% | 23 |
| November | $2.22 | 40% | 22 |
| December | $2.28 | 42% | 30 |

December has the most negative-spread days of any month, cold enough to spike gas, but often not cold enough to push power prices high enough to compensate. The rare exception: when a proper freeze arrives, like January 2026.

[![Seasonal Patterns — Average Monthly Spark Spread + % of Day Profitable](/blog/assets/images/blog_images/what-spark-spread-tells-you-about-texas-grid-stress/the_texas_grid_rhythm.png)](/blog/assets/images/blog_images/what-spark-spread-tells-you-about-texas-grid-stress/the_texas_grid_rhythm.png){:target="_blank"}

The charts show the economics: August dominates with $20/MWh CCGT spreads, 86% profitable intervals. Shoulder months dip negative. Peakers struggle everywhere except summer peaks.

Peakers burn 43% more gas per MWh, so they need much higher prices to break even. They exist because August profits cover the dead months. The spark spread tells you exactly when the grid is stressed and how much plants are making (or losing).

---

## The Demand Side Mirror: What 4CP Has to Do With It

Gas plant operators aren't the only ones watching the spark spread. Every large industrial customer in Texas, such as refineries, petrochemical plants, data centers, and aluminum smelters, has someone whose entire job in summer is monitoring ERCOT load in real time.

The reason is something called **[Four Coincident Peaks (4CP)](https://medium.com/industrial-sun-insights/understanding-ercots-4cp-demand-charge-759c02034120)**. Each year, ERCOT identifies the 4 highest 15-minute demand intervals during June through September. Those four moments determine each large customer's share of transmission charges for the following 12 months. For a major industrial facility, the bill can run into millions of dollars. Getting caught at full load during a 4CP event or curtailing prematurely on a false alarm has significant financial consequences.

In a [blog](https://medium.com/industrial-sun-insights/understanding-ercots-4cp-demand-charge-759c02034120) I read, they provided an example where 'Centerpoint customers paid $56.51/4CPkw, which is $56,510/MWh during the 4CP times. For a 50 MW industrial load, that becomes **$2,825,500** for a single hour’s worth of power'. The financial implications can be huge!

In one of the tables we have generated we have a column called `economic_ratio_ccgt` that represents the ratio of intervals where the spark spread for a CCGT (Combined Cycle Gas Turbine) plant is economically positive compared to the total intervals in a day. On the hottest summer days in our dataset, that ratio hits **1.0**, meaning all 96 intervals were profitable, power prices stayed elevated all day, and the grid was running tight from open to close. Those are the days when 4CP risk is highest.

The same signal that tells a gas plant operator "run hard all day" tells an industrial energy manager "this might be the one." Generators are sprinting. Industrials are watching every interval. Both are responding to the same underlying condition and that is scarcity on the Texas grid

---

## Building the Data Platform on Databricks

Understanding the patterns across 700+ settlement nodes, 96 intervals per day, two years of history requires real infrastructure.

The platform behind this analysis is built entirely on Databricks using Lakeflow Spark Declarative Pipelines (SDP).

Previously, Lakeflow Spark Declarative Pipelines was called DLT (Delta Live Tables) and I wasn't the biggest fan. Writing tests for your pipelines was difficult and it was hard to test the code (if not impossible) outside the context of DLT. I also found it very difficult to debug pipelines in DLT since the pipelines were such a high-level abstraction. They were also expensive compared to rolling your own Spark code. I was also concerned about vendor lock-in with the tech but that has since been largely addressed with SDP now being [open source](https://www.databricks.com/blog/bringing-declarative-pipelines-apache-spark-open-source-project). I have been pleasantly surprised by SDP especially around the way it handles things like [SCD Type 1 and 2](https://learn.microsoft.com/en-us/azure/databricks/ldp/concepts#what-are-the-benefits-of-sdp) and leveraging things like [@dp.expect_or_drop](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations#what-are-expectations) for data quality checks.

I still like the flexibility of rolling my own framework leveraging PySpark and other open source tools, but I am excited to continue leveraging SDP to ingest and transform data for future energy market blogs like this.

To gather the data necessary to put together this blog, here is the architecture that was built. From ERCOT hub prices, Henry Hub gas, and Texas weather to a daily spark spread signal:

{% include spark_spread_diagram.html %}

> Note: I am experimenting with animated diagrams, let me know what you think!

---

## Conclusion

It's cool how much insight can come from combining a simple market concept with the right data infrastructure. The spark spread is a straightforward calculation, but when you view it across thousands of settlement points, weather events, fuel markets, and seasonal demand patterns, it becomes a powerful lens into how the Texas grid behaves under stress.

This project also turned into a great excuse to experiment with a modern data stack. Using Databricks SDP, I was able to ingest and model data from multiple sources including ERCOT market data, natural gas prices, weather feeds, and EIA datasets. Bringing these together in a medallion-style architecture made it easy to iterate quickly, test new ideas, and explore the relationships between weather, fuel costs, and electricity prices.

Another surprisingly helpful part of this journey has been working with Claude Code and a few MCP servers. Having an AI assistant available while exploring a new domain made it much easier to understand unfamiliar energy market concepts, locate useful datasets, and quickly prototype analysis pipelines. It has felt less like searching for information and more like collaborating with a research assistant while building the platform.

This is still very much the beginning of the exploration. I'm currently experimenting with bringing in additional datasets and expanding the platform to look at other ERCOT signals such as nodal congestion, real-time price spikes, and transmission constraints. There is a lot of interesting structure in these markets, and the combination of modern data platforms and AI-assisted development makes it easier than ever to dig into it.

Thanks for reading 😊!
