#!/bin/bash

set -e

PROJECT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

cd "$PROJECT_DIR"

echo "Starting Linux Disk Investigator..."

python3 app.py \
    --path "${1:-/}" \
    --threshold "${2:-80}"

echo "Investigation completed."