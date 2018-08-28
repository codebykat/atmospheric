Will take photos in the import/ folder and generate a static site that lives in docs/ (for hosting on Github pages).

1. python3 -m venv .virtualenv
1. source .virtualenv/bin/activate
1. brew install libtiff libjpeg webp little-cms2
1. pip install -r requirements.txt
1. python3 generate.py
