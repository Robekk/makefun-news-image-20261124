# The World Today — 24 November 2026 in one image

Entry for the make.fun bounty **"Sum up 24 November's world news in one image"**
(news-image-20261124).

[![Competition](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/Robekk/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/Robekk/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-page broadsheet front page that sums up the world news of Tuesday
24 November 2026: Ukraine's war reaching the Mediterranean, Seoul scrambling
jets over Russian planes, the UN's one-year AI-rules call, the EU's 22nd
sanctions package, NATO's space-defence vow, the Senegal migrant-boat
tragedy, and more from the day's wires.

## How it works

- `entry.png` — the front page, drawn with `build_poster.py` (Pillow).
- `main.py` — the entry program: standard library only, no network. It
  copies the committed `entry.png` to the output directory as
  `entry.png`, byte for byte, on every run.

## Run

```sh
python3 main.py            # writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR)
```
