# The World Today — 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/jhonrudi12/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/jhonrudi12/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A newspaper-style front page that sums up the world news of **Monday 23 November 2026** in one image, built for the [make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123).

## The day in six stories

1. **COP31 collapses without a deal** — after two weeks of talks and two days of overtime in Antalya, the longest climate summit ever ends with no agreement, the first collapse since Copenhagen in 2009; the draft never named fossil fuels.
2. **Democrats win a record House majority** — 258 seats, their biggest since 1992, as Chuck Hubbard beats Rep. Virginia Foxx in North Carolina; a gain of 44 seats sets up divided government.
3. **Russian warship hit off Libya** — suspected Ukrainian sea drones badly damage the corvette Merkury at Benghazi, days after a Russian cargo ship was hit in the Baltic.
4. **Factory fire: 50 missing in Java** — seven body bags recovered and about 50 workers missing after fire guts a candy factory in Serang, west Java.
5. **Minister quits over AI exam cheating** — South Korea's Education Minister Choi Kyo-jin resigns after last-minute anti-cheating rules sow chaos before the college entrance exam.
6. **Nepal PM meets Modi in Delhi today** — Balendra Shah's first bilateral trip abroad since taking office in March; trade, energy and connectivity top the agenda.

Plus: a drone strike on a flat near Kyiv leaves 14 missing in Dymer, and Trump vows to work with Democrats to cap credit-card interest at 10%.

Sources: AP, Reuters, CNN, Yonhap, MEA (early edition, stories reported by 07:30 WIB, 23 Nov 2026).

## How it works

`main.py` is a pure Python 3.13 standard-library program: it draws the whole front page — masthead, headlines, summaries and icons — with an embedded 5x7 bitmap font and simple shapes, and writes a deterministic 1024×1024 PNG to `/output/entry.png`. No network, no fonts, no image libraries, so two runs produce identical bytes.

## Run it

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024, under 1 MiB)
```

## License

MIT — see [LICENSE](LICENSE).
