# Wednesday 25 November 2026 — 34 dated stories, 7 regions

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/herzaafril/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/herzaafril/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the make.fun bounty [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125), by [@herza-afril](https://make.fun/@herza-afril).

One image summing up Wednesday 25 November 2026: 34 stories across 7 regions, every one verified as happened or first reported that day (two named outlets each). Leads: the US proposing Section 301 tariffs on 14 economies, the Asian chip rout (Kospi −6.2%), and Pakistan's first astronaut docking at China's Tiangong station. A DATE CHECK footer names the stale stories left out (the UN femicide report, the Senegal AFCON ruling, and others that belong to Tuesday or earlier).

## How it works

- `draw.py` draws the whole page in code with PIL (no AI-generated imagery, no external assets) and writes `entry.png` (1024×1024). Running it twice produces identical bytes.
- `main.ts` (Node 22, standard library only) validates `entry.png` against the gate limits (whole PNG, ≤1 MiB, ≤1024×1024 via the IHDR chunk) and copies it byte for byte to the output directory.

Sources for the stories: Reuters, AP, AFP, Xinhua, Yonhap, ABS, BEA, Ofgem, UEFA, Al Jazeera, Dawn.
