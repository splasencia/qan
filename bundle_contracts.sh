#!/bin/bash

set -e

# Input and output directories
CONTRACTS_DIR="/contracts"
OUTPUT_DIR="/bundled_contracts"

# Ensure output directory exists
mkdir -p $OUTPUT_DIR

# Iterate through all Solidity files in the contracts directory
for contract in $CONTRACTS_DIR/*.sol; do
    # Define output file path
    output_file="$OUTPUT_DIR/$(basename $contract)"

    # Run the bundler script
    python3 /app/bundler.py "$contract" "$output_file" --node-modules-path /app/node_modules
    echo "Bundled $(basename $contract) -> $output_file"
done

echo "All contracts bundled successfully."

