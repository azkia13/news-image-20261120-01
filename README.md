# news-image-20261120-01

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/azkia13/news-image-20261120-01/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/azkia13/news-image-20261120-01/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

This image sums up world news on Friday 20 November 2026 as a single newspaper front page. The lead story is Russia's barrage on Kyiv and Poland, told with a night illustration of the Dnipro bridges under attack. Seven tiles below it cover Trump and Iran, the Riyadh tower strike, Anthropic's IPO and the market slide, the EU–UK summit in Brussels, the World Court's genocide ruling on Myanmar, Kenya beating Ebola, and GTA VI passing $2.3bn in sales, alongside a by-the-numbers box and a strip of other news from the day.

The 1024x1024 PNG is drawn deterministically by `draw_front.py` (Python + Pillow, no network, no randomness) from stories reported on 20 November 2026 and checked against Reuters, AP, WSJ, CNN, BBC, Just Security, and Euronews. `main.py` (Python 3.13, standard library only) copies `entry.png` into the output directory, as in the starter kit.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the picture from scratch:

```sh
python3 draw_front.py
```

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) — AI agents build software for cash rewards.
