---
title: "The Meta-Harness: One Layer to Rule Every AI Coding Agent"
date: 2026-08-16T10:00:00-04:00
categories:
  - GenAI
tags:
  - Omnigent
  - Databricks
  - AI Agents
  - Self-Hosting
  - Energy
---

{% raw %}<img src="/blog/assets/images/blog_images/the-meta-harness-one-layer-to-rule-every-ai-coding-agent/blog_image.jpeg" alt="">{% endraw %}

I've been pretty excited about Omnigent and I have been using it a fair bit lately both at work and for personal use. It solves a problem I honestly did not know I had but now that I am using it more and more, I am thankful there is a tool out there to address it. The problem being, how do we orchestrate a task across multiple agents between many different harnesses?

I set it up on my WSL machine at home after getting tired of context-switching between Claude Code, Cursor, and OpenCode on the same project. I was also looking for options to interact with my agents via my phone in an easy way.

In my [last blog](https://schiiss.github.io/blog/energy/mapping-global-gas-flow-with-omnigent/), I used Omnigent to orchestrate multiple agents across a few different harnesses to create a global gas flow map on top of Databricks Free Edition and touched on what makes it interesting at a high level. In this post, I wanted to go a bit deeper. Specifically into the self-hosting story and the concept that I think is the most architecturally interesting thing Omnigent does: the **meta-harness**.

Omnigent is still in alpha and I ran into a non-trivial number of issues getting this setup working. I wanted to spend some time covering my setup and how I am hosting my Omnigent server on my local network, and exposing it so I can access it from anywhere.

The primary use case I will use to anchor this blog will revolve around keeping up to date with the latest happenings in energy markets. Many of my customers work in the energy/oil and gas sector and many of the folks I work with are in the commodity trading or marketing space. To make sure I am equipped to talk to them, I have been pulling all kinds of energy market data into my Databricks Free Edition workspace and now I have Omnigent generate me a daily market report that ties into data on my lakehouse.

---

## The Emerging Harness Problem

Most AI coding content I see right now is about *using* one of the big tools out there on the market. Tools like Claude Code, Codex, Cursor, Goose, OpenCode. Pick one, follow the quickstart, and you're off to the races.

The problem I am seeing with customers is that nobody uses just one. I've seen teams running a mix of tools, and this can complicate things.

- Every tool has its own session model, credential store, and UI
- There's no unified way to enforce cost controls or access policies across all of them
- Collaboration is essentially nonexistent. You can't share a live agent session with a teammate across tools
- If you want to swap runtimes mid-project, you're starting from scratch

This is the gap Omnigent is designed to close. As they put it:

> To combine agents, govern them, and work on them with other people, you need a layer above the harness. Omnigent is that layer.

---

## What Is a Harness?

Before the meta part, it's worth knowing what Omnigent means by a **harness**. It's the runtime abstraction that executes your agent loop. The key idea is that you can swap the underlying agent runtime with a single config line while your tools, prompts, and policies stay unchanged.

There are two execution modes:

- **Direct**: Omnigent itself drives the model and tools, providing streaming, a web UI, persistent sessions, mobile access, and policy enforcement
- **Native TUI**: Omnigent boots the vendor's own terminal interface and mirrors it back, wrapping the native experience with Omnigent's collaboration and policy layer

![Omnigent meta-harness architecture](/blog/assets/images/blog_images/the-meta-harness-one-layer-to-rule-every-ai-coding-agent/omnigent_architecture.png){: style="display:block; margin:0 auto;" }
*CLI and custom agents feed into a sandboxed Runner, which connects to a shared Server holding history, policies, MCPs, artifacts, and skills. You reach that server from any surface: terminal, web, native app, mobile, or REST API.*

So when I run `omnigent claude`, I'm not just launching an instance of Claude Code. I'm launching it inside a managed environment where my session is persisted, my colleagues can join it with a link, and any policies I've configured are enforced.

---

## The Meta-Harness: ACP

The part I find intriguing is something called the `acp` harness, the **Agent Client Protocol** harness. It's different from all the others.

Rather than hardcoding support for a specific tool, `acp` is a generic meta-harness that can drive *any* agent that implements the open Agent Client Protocol, an editor-agnostic spec Zed published in 2025 and later co-developed with JetBrains, which Gemini CLI, Goose, and others have already adopted. You register a launch command, Omnigent negotiates ACP against whatever process starts up, and it surfaces as `acp:<your-slug>` across the entire platform.

```yaml
harnesses:
  my-internal-tool:
    kind: acp
    command: my-internal-agent --serve
```

That's it. Your internal tool, your custom agent, whatever you've built in-house: as long as it speaks ACP, Omnigent treats it identically to Claude Code, Cursor, or OpenCode.

A few things to note here:

- **Omnigent exposes its own built-in tools** (session management, sub-agent spawning, skills, policies) alongside the agent's native tools via an MCP bridge. You can disable this with `OMNIGENT_ACP_MCP=0` if you want a clean separation
- **Harnesses are also pluggable** via a Python entry-point system under the `omnigent.community.harness` group. A third-party package can introduce a new harness without touching Omnigent core. It just declares a `HarnessContribution` object
- **Sessions belong to you, not to the agent**. Start something in Claude Code, fork it, and pick it back up in Cursor or OpenCode. The new agent inherits the full conversation history

The closest analogy I've got is what REST did for APIs. Instead of every team building a custom integration with every tool, you agree on a protocol and the integrations compose.

---

## The Self-Hosted Setup

I wanted to get a proper self-hosted Omnigent instance running on my Windows machine without spinning up cloud infrastructure. Here's what I ended up with.

**The stack:**

| Layer | Choice | Why |
|---|---|---|
| Runtime | WSL2 on Windows | Full Linux environment without a separate VM |
| Orchestration | Omnigent (self-hosted) | Local SQLite, no cloud dependency for the control plane |
| Harnesses | Claude Code, Cursor, OpenCode | Swappable runtimes behind a single Omnigent interface |
| Networking | Tailscale + `tailscale serve` | Zero-config HTTPS across devices, tailnet-only exposure |

The Omnigent install itself is a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/omnigent-ai/omnigent/main/scripts/install_oss.sh | sh
```

On WSL2 you will need `tmux` and `bubblewrap` for the native terminal harnesses, and Node.js 18+ for Claude Code and OpenCode (22+ is the current recommendation). Both were missing on my machine and cost me some time.

---

## The Networking Layer: Tailscale + WSL2

This is where I spent most of my debugging time, so I want to document it properly.

Basically, I wanted to run Omnigent on my WSL2 machine and access it from any device on my Tailscale network, including my phone. Tailscale has a feature called `tailscale serve` that lets you expose a local HTTP service as HTTPS on your tailnet hostname with no certificate management:

```bash
tailscale serve --bg http://localhost:6767
```

After that, an HTTP endpoint similar to `https://<your-host>.ts.net` proxies straight through to the Omnigent server. In theory.

In practice, three things broke before I got it all working:

**1. The CORS enforcement**

Omnigent's server runs in local single-user mode by default, which means it only trusts requests with a loopback `Origin` header (`127.0.0.1`, `localhost`). When your browser sends `Origin: https://<your-host>.ts.net`, the server rejects it with a 403:

> Forbidden: this endpoint requires a trusted Origin header. It accepts multipart uploads, which are CORS-safelisted, so a trusted Origin is required to prevent cross-site request forgery.

The fix is an environment variable:

```bash
export OMNIGENT_WS_ALLOWED_ORIGINS=https://<your-host>.ts.net
```

Add it to `~/.zshrc` so it persists and gets inherited by the background server process.

**2. The WSL2 iptables gap**

Tailscale logs a health warning on WSL2 about missing `CONNMARK` kernel modules. The WSL2 kernel does not ship with all the netfilter modules Tailscale expects. Running with `--netfilter-mode=off` resolves the warning:

```bash
sudo tailscale up --netfilter-mode=off
```

Once I had this all working, I installed the tailscale app on my phone, and I was easily able to access my Omnigent server from anywhere!

---

## Leveraging Omnigent On the Go

If you've been following my blog, you know I've started to dive deeper into energy related concepts and looking at things like ERCOT, LNG gas flow, spark spreads, etc., and I've been pulling lots of energy markets data into my Databricks Free Edition environment.

There's a quote that really resonates with me at Databricks: 'enterprise AI doesn't suffer from an intelligence deficit, but rather a context deficit.' If all your data sits and is exposed in a lakehouse, Databricks is a great tool to act as that context layer.

Every morning when I wake up, I usually take 30 to 45 minutes to catch up on what's happening in energy in Canada and across the globe. That brief read on my phone beats 30 minutes of scanning various data sources.

I set this up as an Omnigent [scheduled task](https://omnigent.ai/docs/build/scheduled-tasks#scheduled-tasks) that fires each morning. The prompt wires the agent to my lakehouse running on the Databricks Free Edition via the Databricks MCP `execute_sql` tool and runs ten queries: commodity OHLCV, ERCOT spark spreads, system load, weather by load zone, nat gas storage, crude inventory, EIA STEO forecasts, news sentiment, and Substack coverage.

The output is designed to be read on a phone with short tables, bullet points per market segment, and a closing synthesis that connects the dots across all ten data sources.

Here's what a typical morning looks like:

---

# EnergyIQ Daily Brief

**Wednesday, August 12, 2026**

---

## Commodities

|             | Price          | DoD      | 20d Vol |
| ----------- | -------------- | -------- | ------- |
| WTI Crude   | $84.17/bbl     | +2.48%   | 62.46%  |
| Brent Crude | $89.81/bbl     | +2.38%   | 72.04%  |
| Henry Hub   | $2.761/MMBtu   | -1.18%   | 35.83%  |
| RBOB Gas    | $2.913/gal     | **-7.09%** | 53.66% |

---

## ERCOT Power

- **HB_NORTH avg**: $24.64/MWh (range: -$0.33–$85.04)
- **CCGT spark spread**: $5.31/MWh | 7d avg: $8.36/MWh
- **Economic dispatch**: 53.9% of intervals gas-fired generation was profitable
- **System load**: 83,118 MW peak | 70,891 MW avg (-3,752 MW peak / -456 MW avg vs same day last week)

---

## Weather (ERCOT Zones)

| Zone | City | High (°F) | Daily CDD | 7d Rolling CDD |
|------|------|-----------|-----------|----------------|
| LZ_NORTH | Dallas | 99.1 | 23.8 | **170.2** ⚑ |
| LZ_WEST | Midland | 97.1 | 21.5 | 150.6 |
| LZ_SOUTH | Corpus Christi | 91.9 | 20.9 | 142.9 |
| LZ_HOUSTON | Houston | 89.2 | 18.0 | 135.0 |

LZ_NORTH (Dallas) leading all zones at 170.2 rolling 7d CDD — sustained triple-digit heat.

---

## Natural Gas

- **L48 storage**: 3,117 Bcf | WoW: +33 Bcf | vs year-ago: -13 Bcf
- **Henry Hub**: $2.747/MMBtu (storage report close)

## Crude Oil

- **US crude stocks**: 711,796 MBBL | WoW: -362 MBBL (second straight draw; prior week -10,964 MBBL)
- **US crude production**: 13,804 Mbbl/d (EIA weekly, week of Jul 31)

---

## News Sentiment

**Tone**: 1 bullish / 2 bearish / 1 neutral across 4 articles

- [Crude Prices Soar as Strait of Hormuz Reopening in Doubt](https://www.barchart.com/story/news/3761838/crude-prices-soar-as-strait-of-hormuz-reopening-in-doubt) — Barchart [BEAR]
- [Crude Prices Soar as Middle East Tensions Curb Global Oil Supplies](https://www.barchart.com/story/news/3758309/crude-prices-soar-as-middle-east-tensions-curb-global-oil-supplies) — Barchart [BEAR]
- [Nat-Gas Prices Surge on Hot US Weather Forecasts](https://www.barchart.com/story/news/3761809/nat-gas-prices-surge-on-hot-us-weather-forecasts) — Barchart [BULL]
- [OpenAI backs Abbott's audit of Texas AI data center projects](https://4sysops.com/archives/openai-backs-abbotts-audit-of-texas-ai-data-center-projects/) — 4sysops [NEUT]

---

## Substack Radar

- [**The Zawiya Escalation: Libya's Energy Infrastructure Under Attack**](https://energygeopoliticsandstatecraft.substack.com/p/the-zawiya-escalation-libyas-energy) (Energy Geopolitics & Statecraft, Francesco Sassi): Drone strikes on the Zawiya refinery causing oil losses and fuel shortages; NOC warns of deteriorating security with output nearing record highs. [BEAR]
- [**Enbridge Unveils Wrangler Pipeline: Direct Capacity from Wyoming to Cushing**](https://www.plainview-energy.com/p/enbridge-unveils-wrangler-pipeline) (A Plainview on Crude Oil, Plainview Energy Analytics): New leased-capacity product combines Platte + Spearhead into one streamlined Wyoming-to-Cushing lane, competing with Pony Express and Saddlehorn. [BULL]
- [**Big Tech's Big Fumble**](https://energybadboys.substack.com/p/big-techs-big-fumble) (Energy Bad Boys, Mitch Rolling): 300+ data center bans across the US; Big Tech's green energy advocacy is backfiring as rising electricity prices and thinning reserve margins draw backlash. [BEAR]
- [**Inside Enbridge's Pipeline Expansion: How MLO1 & MLO2 Will Move Incremental Canadian Barrels**](https://www.plainview-energy.com/p/inside-enbridges-pipeline-expansion) (A Plainview on Crude Oil, Plainview Energy Analytics): Southern Illinois Connector handles 100k bpd; MLO2 upstream delayed but downstream prioritized to unlock up to 250k bpd of Canadian egress. [NEUT]
- [**How Drought and Heat are Reshaping European Power Markets**](https://energygeopoliticsandstatecraft.substack.com/p/today-at-1400-cet-how-drought-and) (Energy Geopolitics & Statecraft, Francesco Sassi): Webinar coverage on climate shocks hitting European hydropower and cross-border flows — parallel theme to the US heat story. [NEUT]

---

## EIA Today in Energy

- [**Hourly peak load in ERCOT set a new record, exceeding 91 GW on July 22**](https://www.eia.gov/todayinenergy/detail.php?id=67906): ERCOT hit 91 GW on Jul 22 — met primarily by natural gas and solar. Puts current 83 GW load in context of a grid already tested near limits this summer. [NEUT]
- [**Battery storage capacity averaged 70% growth over the last three years**](https://www.eia.gov/todayinenergy/detail.php?id=67925): 52 GW installed by mid-2026 with 54 GW more planned; solar-co-located units dominate. [BULL]
- [**Duration of power outages in Puerto Rico increased 19% in 2025**](https://www.eia.gov/todayinenergy/detail.php?id=67926): Average 36 hrs of interruptions vs 2 hrs mainland — grid fragility story. [BEAR]
- [**China's crude oil imports fell in the second quarter**](https://www.eia.gov/todayinenergy/detail.php?id=67905): Down 32% in Q2 2026 to 8.1 Mbbl/d as Hormuz disruptions raised prices; drops from Iraq, Russia, UAE. Demand destruction softening global price effects. [BEAR]
- [**Lower crude oil prices reduced U.S.-Canada energy trade value in 2025**](https://www.eia.gov/todayinenergy/detail.php?id=67904): Total bilateral energy trade fell 11% to $137B in 2025 on lower crude prices and volumes. [BEAR]

---

## Market Pulse

The dominant signal today is a geopolitical crude bid colliding with a sharp RBOB selloff — WTI and Brent both up ~2.5% on Hormuz supply risk, while gasoline cratered 7.1%, the largest single-day move in the dataset, compressing crack spreads hard. The ERCOT power market is not tracking the heat: Dallas at 99°F with 170 rolling CDDs, yet HB_NORTH averaged just $24.64/MWh and gas-fired dispatch was profitable only 54% of the time — down sharply from 85% the prior day — suggesting renewables and storage (52 GW nationally per EIA) are shouldering more of the Texas peak. Henry Hub slipped 1.2% despite the weather headlines, consistent with a storage trajectory still in slight year-ago deficit (-13 Bcf) but injecting above the prior week's pace (+33 vs +28 Bcf); the softness in gas is a mixed signal for spark spreads. Watch the Hormuz-Libya double-supply-shock narrative: Zawiya refinery under drone attack and Hormuz uncertainty appeared in three of four news items — if that premium sticks in crude while cracks stay compressed, refiners are being squeezed on both ends.

---

Paired with the Omnigent [mobile app](https://omnigent.ai/docs/interact/mobile), this lands on my phone and delivers me critical information I need to stay up to date with what's happening in the markets. The context comes from my own Databricks catalog. The agent does the synthesis. I just read it.

![EnergyIQ daily brief on Omnigent mobile, showing Substack Radar with Canadian pipeline coverage](/blog/assets/images/blog_images/the-meta-harness-one-layer-to-rule-every-ai-coding-agent/omnigent_mobile.jpeg){: style="display:block; margin:0 auto; max-width:400px;" }
*The EnergyIQ brief open on my phone via the Omnigent mobile app, pulling from my self-hosted WSL2 instance over Tailscale.*

Running this daily costs around $1.80/month. This includes tokens and compute on the Databricks side.

I also do something similar for the STEO from the EIA that runs once a month to summarize the latest release:

---

# EnergyIQ STEO Monthly Brief

**July 2026 | EIA Short-Term Energy Outlook**
[View full report](https://www.eia.gov/outlooks/steo/archives/jul26.pdf)

---

## Key Forecast Metrics

| Metric | Forecast |
|---|---|
| WTI Price | ~$76/bbl (2026 annual avg); H2 2026 ~$68/bbl; 2027 avg $60.76/bbl |
| Brent Price | $82/bbl (2026 annual avg); H2 2026 ~$72/bbl; 2027 avg $64.76/bbl |
| Henry Hub | $3.67/MMBtu (2026 avg); $3.49/MMBtu (2027 avg) |
| US Oil Production | 13.8 MMbbl/d (2026); 14.0 MMbbl/d (2027) |
| Global Oil Demand | N/A in metadata — see supply/demand balance in Oil section |
| US Electricity | Average ~$45/MWh wholesale; residential retail 18.3¢/kWh (2026) |

> *WTI and global demand fields were null in the metadata JSON; WTI and Brent figures derived from the STEO summary price table. 2026 annual averages are skewed by the Q2 2026 price spike.*

---

## Oil Market Outlook

The dominant story of the July 2026 STEO is an extraordinary Q2 2026 supply shock: OPEC+ total production plunged from 31.45 mb/d in Q1 to 25.95 mb/d in Q2, crushing effective surplus capacity to essentially zero (0.02 mb/d) and catapulting Brent to a quarterly average of $102.93/bbl and WTI to $95.48/bbl — the highest readings in the forecast window. EIA's base case treats Q2 as an acute disruption already unwinding: Q3 2026 OPEC+ output recovers to 28.94 mb/d, Q4 to 32.85 mb/d, and 2027 settles at 33.56 mb/d average (broadly back to 2025 levels). On that path, Brent declines to ~$74 in Q3 2026, ~$70 in Q4, and grinds lower to a 2027 annual average of $64.76/bbl; WTI follows at $60.76/bbl for 2027. US production is a steady counter-force, rising from 13.78 mb/d in 2026 to 14.03 mb/d in 2027 as the Permian stays in build mode. OECD commercial inventories troughed at 2,557 million barrels in Q3 2026 (down from 2,829 mb at end-2025) and rebuild to 3,021 mb by end-2027 — a significant storage build that underpins the bearish 2027 price trajectory.

---

## Natural Gas Outlook

With U.S. working gas inventories sitting 6% above the five-year average at end-June 2026, EIA sees little room for price appreciation near-term: Henry Hub is forecast to average $3.57/MMBtu in Q4 2026, 5% below the same quarter in 2025, before recovering modestly to $3.78/MMBtu by Q4 2027. Full-year averages land at $3.67/MMBtu (2026) and just under $3.50/MMBtu (2027), marginally below the 2025 print of $3.53/MMBtu — a remarkably flat multi-year range. The storage buffer remains intact: EIA projects end-October 2026 inventories of 3,966 Bcf (5% above the five-year average), providing a comfortable cushion into winter. The key demand counterweight is electric power burn, which EIA forecasts rising 2% in 2026 and another 4% in 2027, reaching a record 38.1 Bcf/d for the full year and a single-month all-time peak of 50.6 Bcf/d in July 2027 — driven by rising electricity demand, 508 GW of gas-fired capacity (up 3% from 2025), and gas prices that remain ~10% below their 2016–2025 inflation-adjusted average. LNG export growth is an additional structural demand pull, but above-average storage limits the upside in the near term.

---

## Electricity & Renewables

Solar PV is the undisputed capacity growth story: EIA forecasts U.S. installed utility-scale solar growing from 149.8 GW (Q4 2025) to 181.6 GW (Q4 2026) and 221.1 GW (Q4 2027) — a 47.6% increase in two years — while wind grows more modestly from 158.0 GW to 178.4 GW (+12.9%) over the same period. Solar's growth rate now substantially exceeds wind on an absolute and percentage basis, reshaping seasonal generation profiles and producing the sharpest mid-day grid effects. Coal in the electric power sector continues its structural decline — EIA projects power-sector coal consumption falling from 417 billion short tons in 2025 to 379 billion in 2026 and 366 billion in 2027 — displaced by the combination of cheap gas and rapidly scaling solar. Natural gas fills the residual load role, with summer generation and peak-demand dispatch continuing to be the highest-utilization periods; the gas fleet is being actively expanded (508 GW by end-2027) precisely to backstop renewable intermittency. Retail electricity prices to residential customers are forecast at 18.29¢/kWh in 2026 and 18.70¢/kWh in 2027, modest increases that reflect rising wholesale costs partially offset by efficiency gains.

---

## Global Macro & Demand

OECD-region liquid fuels demand is projected at roughly 25 mb/d for North America (US ~20.7, Canada ~2.5, Mexico ~1.8 mb/d) with little growth through 2027, reflecting a mature demand base. Non-OECD growth is the swing factor, with China holding relatively flat at ~5.5 mb/d of oil production (declining domestic output partially offset by demand growth), while the S&P Global macro model underlying EIA's forecasts implies the U.S. dollar index softening modestly from a 2025 average of 116.4 to 113.4 in 2026 — a mild tailwind for emerging-market demand. The primary downside risk to EIA's demand-side base case is a GDP growth disappointment in the non-OECD block; U.S. macroeconomic forecasts are anchored to S&P Global's model, which appears to embed a soft-landing scenario with no recession.

---

## Analyst Take

The central tension in the July 2026 STEO is between a Q2 2026 oil price spike that appears acute and self-correcting versus a supply structure that, once OPEC+ normalizes, points decisively lower by 2027. EIA's base case — Brent declining from $103 in Q2 2026 to ~$65 annually in 2027 — is directionally defensible, but the trajectory is almost entirely contingent on OPEC+ maintaining the production recovery it has signaled: if the cartel re-cuts rather than restores volumes, inventory builds don't materialize and the $65 Brent floor evaporates. The biggest upside risk to the forecast is embedded in natural gas and power: EIA projects record-breaking power-sector gas burn through 2027, driven by data-center and AI-linked electricity demand growth that it models conservatively; any acceleration in commercial electricity load could push Henry Hub materially above the flat ~$3.50–$3.67 range EIA has penciled in, and would also lift gas-plant capacity utilization well beyond current assumptions. On the electricity side, solar's 47.6% capacity build over two years is among the most aggressive EIA has ever forecast, and any supply-chain friction or permitting slowdown would slow the coal displacement thesis without a gas-price offset. Compared to the prior cycle (2025 averages: WTI $65.40, Brent $69.04, Henry Hub $3.53), the 2026 annual "forecasts" are inflated by the Q2 shock — the more informative directional comparison is H2 2026 (WTI ~$68–71, Brent ~$72–74) versus a 2027 exit rate below $60 WTI — a nearly $10/bbl bear thesis in crude that demands OPEC+ discipline to fail rather than hold.

---

> Note: there are very likely gaps and errors in this summary which is why it is very important to validate AI generated outputs. I still have lots of work to do on the data side to make sure this is all accurate.

---

## What Is Next

A few things I didn't get to in this post:

- **Multi-agent sessions via ACP**: routing a task between Claude Code and Cursor based on context mid-session. Omnigent has two built-in agents for this: **Polly** (a multi-agent coding orchestrator that breaks tasks into sub-tasks and delegates each to a different agent) and **Debby** (a multi-model brainstorming partner that fans a question out to multiple harnesses simultaneously and lets them debate the answer). I haven't used either one in a real project yet
- **Custom harness plugin**: wrapping an internal tool as an ACP-compliant agent via the Python entry-point system
- **MLflow Tracing integration**: getting agent observability into the same traces I am already collecting for other GenAI workloads
- **Smart routing via Unity AI Gateway**: Databricks just [announced](https://www.databricks.com/blog/smart-routing-unity-ai-gateway-match-frontier-quality-30-lower-cost-task) a beta that classifies task complexity at session start and routes to the right model automatically. Their numbers are 30%+ lower cost with matched frontier quality on internal workloads. What I find interesting is that routing extends beyond models to harnesses too, so Omnigent could eventually let Databricks decide not just which model handles a sub-task but which agent runtime. That's the meta-harness story taken one level further and I'm watching it closely.

Omnigent is still alpha and rough in places, but the architecture is sound. If more tools adopt ACP, this gets very interesting very fast.

Thanks for reading 😃
