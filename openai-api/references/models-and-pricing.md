# Models and pricing

> Snapshot from https://developers.openai.com/api/docs/pricing, taken **2026-09-25**.
> OpenAI revises model lineups and prices frequently — re-fetch that page before quoting a
> number that matters (a cost estimate someone will act on, a model pinned in code).

All prices are **USD per 1M tokens**. "Cached" is the price for input tokens that hit
OpenAI's automatic prompt cache (see [prompt-caching.md](prompt-caching.md)) — routinely
~10% of the standard input price. Batch API pricing is a flat 50% off both input and output
for any model, for asynchronous jobs that complete within 24 hours.

## Flagship — GPT-6 series

| Model | Input | Cached input | Output |
|---|---|---|---|
| `gpt-6-astra` | $10.00 | $1.00 | $50.00 |
| `gpt-6-sol` | $2.00 | $0.20 | $10.00 |
| `gpt-6-luna` | $0.10 | $0.01 | $0.50 |

`astra` is the current top-of-lineup flagship (released 2026-09-03). `sol`/`luna` are the
mid- and low-cost tiers of the same generation.

## GPT-5.x series

| Model | Input | Cached input | Output |
|---|---|---|---|
| `gpt-5.6-sol` | $4.00 | $0.40 | $20.00 |
| `gpt-5.6-terra` | $2.00 | $0.20 | $12.00 |
| `gpt-5.6-luna` | $0.20 | $0.02 | $1.20 |
| `gpt-5.5` | $5.00 | $0.50 | $30.00 |
| `gpt-5.5-pro` | $30.00 | — | $180.00 |
| `gpt-5.4` | $2.50 | $0.25 | $15.00 |
| `gpt-5.4-pro` | $30.00 | — | $180.00 |
| `gpt-5.4-mini` | $0.75 | $0.075 | $4.50 |
| `gpt-5.4-nano` | $0.20 | $0.02 | $1.25 |
| `gpt-5.2` | $1.75 | $0.175 | $14.00 |
| `gpt-5.2-pro` | $21.00 | — | $168.00 |
| `gpt-5.1` | $1.25 | $0.125 | $10.00 |
| `gpt-5` | $1.25 | $0.125 | $10.00 |
| `gpt-5-pro` | $15.00 | — | $120.00 |
| `gpt-5-mini` | $0.25 | $0.025 | $2.00 |
| `gpt-5-nano` | $0.05 | $0.005 | $0.40 |

`gpt-5.6-sol` was running promotional pricing of $4/$20 through at least 2026-11-21 at time
of writing — check the live page for whether that's still in effect.

## Reasoning models (o-series)

Slower and far more expensive than the GPT-5.x/6 line; the premium buys deeper multi-step
reasoning, not general capability.

| Model | Input | Cached input | Output |
|---|---|---|---|
| `o1` | $15.00 | $7.50 | $60.00 |
| `o1-pro` | $150.00 | — | $600.00 |
| `o3` | $2.00 | $0.50 | $8.00 |
| `o3-pro` | $20.00 | — | $80.00 |
| `o3-mini` | $1.10 | $0.55 | $4.40 |
| `o4-mini` | $1.10 | $0.275 | $4.40 |

## GPT-4 series (legacy, still served)

| Model | Input | Cached input | Output |
|---|---|---|---|
| `gpt-4.1` | $2.00 | $0.50 | $8.00 |
| `gpt-4.1-mini` | $0.40 | $0.10 | $1.60 |
| `gpt-4.1-nano` | $0.10 | $0.025 | $0.40 |
| `gpt-4o` | $2.50 | $1.25 | $10.00 |
| `gpt-4o-mini` | $0.15 | $0.075 | $0.60 |
| `gpt-4o-2024-05-13` | $5.00 | — | $15.00 |
| `gpt-4-turbo-2024-04-09` | $10.00 | — | $30.00 |
| `gpt-4-0613` | $30.00 | — | $60.00 |

## Other

- **Cyber models** (`gpt-5.6-cyber`, `gpt-5.5-cyber`): $12.50 / $1.25 cached / $75.00 —
  specialized, priced near the top of the range. Confirm the use case actually needs the
  specialized model before recommending it.
- **Legacy completion models** (`gpt-3.5-turbo`, `davinci-002`, `babbage-002`): still listed,
  rarely the right choice for new work.

## Picking a tier

Match spend to what the task needs — see [SKILL.md](../SKILL.md#model-choice-at-a-glance)
for the quick heuristic. A `nano`/`luna` model on high-volume classification vs. a `-pro`
reasoning model on the same task is a 100–1000x cost difference for work that usually doesn't
need the reasoning depth.
