Will take photos in the import/ folder and generate a static site that lives in docs/ (for hosting on Github pages).

Stack:
* <a href="https://www.python.org/">Python3</a>
* <a href="http://jinja.pocoo.org/">Jinja2</a>
* <a href="https://pillow.readthedocs.io/en/5.2.x/">Pillow</a>
* <a href="https://github.com/tqdm/tqdm">tqdm</a>

Build instructions:
1. Create a virtualenv. `python3 -m venv .virtualenv`
1. `source .virtualenv/bin/activate`
1. Install dependencies for Pillow: `brew install libtiff libjpeg webp little-cms2`
1. `pip install -r requirements.txt`
1. `python3 generate.py`
