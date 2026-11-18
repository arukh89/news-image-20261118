"""Grader entrypoint: write the news poster to the output directory.

The poster itself is entry.png beside this file. It was drawn by
render.py (Pillow, build time only) from reporting published on
18 November 2026; this program only copies those exact bytes, so
every run writes the same file. Standard library only, no network,
no clock, no randomness: the output depends on nothing but the
committed image.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(OUTPUT_DIR, "entry.png")

if not os.path.isfile(SOURCE):
    raise SystemExit("entry.png is missing beside main.py")

os.makedirs(OUTPUT_DIR, exist_ok=True)
shutil.copyfile(SOURCE, TARGET)
