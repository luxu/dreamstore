#!/usr/bin/env bash

echo "Building project packages..."
python3 -m pip install --upgrade uv

echo "uv Update to version last..."
uv self update

echo "Building project packages..."
uv venv

echo "Migrating Database..."
python3 manage.py migrate --noinput
