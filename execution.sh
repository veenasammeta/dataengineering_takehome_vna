#!/bin/sh

echo "downloding all the dependencies"
pip install -r requirements.txt

echo  "starting python script"
python3 scripts/main.py

echo "winding down"