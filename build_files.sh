#!/usr/bin/env bash

echo "Building project packages..."
python3 -m pip install --upgrade uv

echo "Building project packages..."
pip install -r requirements.txt

echo "Migrating Database..."
python3 manage.py migrate --noinput
