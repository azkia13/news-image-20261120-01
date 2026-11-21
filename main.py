"""Entrypoint for news-image-20261120.

The front page itself is drawn at build time by draw_front.py and
committed as entry.png. This program does nothing but put that exact
file where the grader reads it, using the standard library alone:
no fonts, no network, no drawing, so the two graded runs can only
produce identical bytes.
"""

import os
import shutil
import sys

IMAGE = "entry.png"


def out_dir():
    """Grader output dir: the kit's env var, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE)
    dest_dir = out_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, IMAGE)
    shutil.copyfile(src, dest)
    if os.path.getsize(dest) != os.path.getsize(src):
        print("copy failed: sizes differ", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(run())
