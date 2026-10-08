# How to Scrape Tennis Explorer: ATP & WTA Matches, Scores and Odds

> **Run it now, no code: [tennisexplorer-scraper on the Apify Store](https://apify.com/bibian/tennisexplorer-scraper)** &nbsp;|&nbsp; $4.50 per 1,000 matches &nbsp;|&nbsp; no browser, no proxy

Scrape ATP and WTA tennis match results, upcoming matches and pre-match odds from Tennis Explorer, and get clean structured data: tournament, players, set scores and betting odds for singles and doubles. Tennis Explorer has no public export and no official API for third parties. This guide shows how to get its match data as clean structured data, with a free Apify Actor, from the console or from code.

Searches this page answers: tennis explorer scraper, atp wta match results api, tennis odds scraper, tennis match data scraper.

## What you get from the Tennis Explorer scraper

- Every match, finished or upcoming, with tournament, round, both players and the final score.
- Pre-match betting odds for both players, when Tennis Explorer publishes them.
- Set-by-set scores (up to 5 sets), the winner, and player seedings.
- ATP and WTA, singles and doubles, switched by a single input field.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five finished matches) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `tour`, `matchType` | `ATP` or `WTA`, and `singles` or `doubles` |
| `date`, `time`, `status` | Match date, kickoff time as shown on the site, and `scheduled`, `live`, `finished` or a walkover/retirement flag |
| `id`, `url` | Tennis Explorer match id and detail page link |
| `tournament`, `tournamentUrl` | Tournament name and link |
| `player1`, `player1Url`, `player1Seed` | First player's name, profile link and seed (null if unseeded) |
| `player2`, `player2Url`, `player2Seed` | Second player's name, profile link and seed |
| `winner` | `1` or `2`, or `null` before the match is finished |
| `setsPlayer1`, `setsPlayer2` | Arrays of up to 5 set scores; unplayed sets are `null` |
| `resultPlayer1`, `resultPlayer2` | Sets won by each player |
| `oddsPlayer1`, `oddsPlayer2` | Pre-match odds, `null` when the site has none for that match |

## Use cases

- **Track results daily**: pull finished matches for the last few days, with full set scores and the winner.
- **Watch upcoming matches and odds**: get scheduled and live matches with their pre-match odds before they start.
- **Feed a betting or stats model**: odds plus set-by-set scores in one normalized record, for ATP and WTA, singles and doubles.
- **Follow a tour level**: Futures, Challengers and main tour are all covered, so you can track a player's whole season.

## Input

| Field | What it does |
|---|---|
| `type` | Tour and draw: `atp-single`, `atp-double`, `wta-single` or `wta-double`. |
| `mode` | `results` reads finished matches going backward from today. `upcoming` reads scheduled and live matches with pre-match odds, going forward from today. |
| `days` | How many calendar days to read (default 3). |
| `maxItems` | The run stops once this many matches are saved (default 50). |

Example input:

```json
{
  "type": "atp-single",
  "mode": "results",
  "days": 3,
  "maxItems": 50
}
```

## Three ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/tennisexplorer-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (tour, mode, number of days and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily results feed, open **Schedules**, create a daily schedule for the Actor and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/tennisexplorer-scraper').call({
    "type": "atp-single",
    "mode": "results",
    "days": 3,
    "maxItems": 50
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.tournament} | ${item.player1} vs ${item.player2} | ${item.resultPlayer1}-${item.resultPlayer2}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/tennisexplorer-scraper").call(run_input={
    "type": "atp-single",
    "mode": "results",
    "days": 3,
    "maxItems": 50,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{item['tournament']} | {item['player1']} vs {item['player2']} | {item.get('resultPlayer1')}-{item.get('resultPlayer2')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

## Pricing

Pay per result: **$4.50 per 1,000 matches** (that is $0.0045 per match), plus a tiny start fee of $0.00005 per run. You pay only for the results saved to the dataset. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/tennisexplorer-scraper) when this guide was written; the Store page is the reference.

## Why this one

- **Cheaper than the installed leader.** $4.50 per 1,000 matches against $7.50 for the only other Tennis Explorer actor on the Store.
- **Results, upcoming matches and odds in one actor.** No need to run a separate tool for pre-match odds.
- **Singles and doubles, ATP and WTA.** One input field switches between all four draws instead of four separate actors.

## Limits and honest notes

- `time` is the kickoff time as Tennis Explorer displays it; the site does not publish a timezone, so treat it as local to the tournament unless you already know it.
- `oddsPlayer1` and `oddsPlayer2` are only published for matches the site has odds for (mostly main tour and upcoming matches); they are `null` otherwise.
- A retired or walkover match is flagged in `status`; its remaining sets are `null`.
- Only players' public match results and seedings are collected: no contact details of any kind.
- This is an unofficial tool, not affiliated with Tennis Explorer. Check the site terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy?**
No. The Actor reads the data directly, so runs are fast and cheap.

**How do I get yesterday's results only?**
Set `mode` to `results` and `days` to `1`, and schedule the Actor once a day.

**Can I get doubles matches?**
Yes, set `type` to `atp-double` or `wta-double`.

**Can I get the data in Excel or Google Sheets?**
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open tennisexplorer-scraper on the Apify Store](https://apify.com/bibian/tennisexplorer-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
