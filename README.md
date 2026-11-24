# THE WORLD IN ONE DAY — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/competitions/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/rank.svg)](https://make.fun/competitions/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/reward.svg)](https://make.fun/competitions/news-image-20261124)

A single 1024×1024 image that sums up Tuesday 24 November 2026's world news:
**60 stories across 7 regions**, in one newspaper front page.

## What's on the page

- **3 large illustrated leads** — Asia rallies as Jensen Huang returns to Nvidia;
  the US blacklists Singapore-based Megaspeed; Zelensky warns Russia is planning
  new strikes.
- **10 small illustrated cards** — Canada–Qatar pact, Moscow's warning to Estonia,
  Iran vowing to fight the blockade, Gaza "a toxic wasteland" (Oxfam), singer
  Parastoo Ahmadi flogged 74 times, Trump's meme-coin gala, Armenia's new
  constitution, Denmark's school phone ban, Oettinger's 5th shutout, UK PMI.
- **47 more stories** in the index, every one with a named source.
- **Numbers band** — Kospi +6.3%, Nvidia +31%, 153/134 drones, $12.2bn,
  99% of Gaza, 24 dead in the Indonesia factory fire.
- **Day by the Clock** — a UTC timeline strip, honest times only; the Ukraine
  23–24 Nov overnight tally is marked PENDING (not yet published at press time).
- **Where It Happened** — a numbered dotted world map with place labels.
- **The Drone War, Night by Night** — bar chart from the Ukrainian Air Force
  (via Ukrinform), with the 23–24 night shown as unknown, not invented.
- **DATE CHECK** — 14 lookalike stories that are NOT 24 Nov news (COP31 collapse,
  Huang's reinstatement, Kilauea ep. 57, the Zaporizhzhia clinic strike, and more),
  plus **NOT YET HAPPENED** and **WHAT TO WATCH ON WEDNESDAY**.

Every story was verified against Reuters / BBC / Bloomberg / Yonhap / AP before
drawing. Unverified claims are flagged [CLAIM]; forecasts [FORECAST]. Nothing
was invented — where the day's data was not yet published, the image says so.

## How it is built

`render.py` draws everything from scratch with Pillow — flat code-drawn
illustrations, no photos, no network, no randomness. Running it twice produces
byte-identical output:

```sh
python3 render.py   # writes entry.png (1024x1024, < 1 MiB)
```

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`).

## License

MIT — see [LICENSE](LICENSE).
