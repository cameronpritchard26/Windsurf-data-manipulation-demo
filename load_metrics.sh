#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: ./load_metrics.sh <date>"
  echo "  date format: yyyy-mm-dd (e.g., 2026-02-12)"
  exit 1
fi

DATE="$1"
INPUT_FILE="myapp_metrics_load-${DATE}.csv"

if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File $INPUT_FILE not found."
  exit 1
fi

# Skip header line, read each row
tail -n +2 "$INPUT_FILE" | while IFS=',' read -r indicator since until good bad total; do
  echo "Processing until: $until"

  curl -k -X 'PUT' \
    "http://localhost:8000/indicators/${indicator}/metrics" \
    -H 'Content-Type: application/json' \
    -d "[
  {
    \"bad\": ${bad},
    \"duration\": 3600000000000,
    \"good\": ${good},
    \"since\": \"${since}\",
    \"total\": ${total},
    \"until\": \"${until}\",
    \"valid\": true
  }
]"

  echo ""
done

echo "Done. All metrics loaded for $DATE."
