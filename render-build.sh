#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip to ensure latest build system matches
python -m pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt
