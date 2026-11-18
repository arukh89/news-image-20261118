# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/arukh89/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/arukh89/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world news of Wednesday 18 November 2026: 41 stories across six continents — a lead story on the Gulf strikes, picture panels for the fallen Crimea bridge span, the Shenzhen summit, the Alaska Senate result and Cyclone Xavier, six small picture cards (Voyager 1, the COP31 talks, the EU's Ukraine loan, the Caracas pact, the IPL retention lists, Nvidia's results), a schematic world map, and a numbered index of 30 more stories. Every shape and letter is drawn from code; no photograph or downloaded artwork is used.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png`, a 1024 by 1024 PNG. To redraw the poster from scratch, run `python3 render.py` (needs Pillow, build time only); it rewrites `entry.png` in this directory. The grader runs only `main.py`, which copies the committed image with the standard library alone, so two runs always write the same bytes.

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
