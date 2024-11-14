#!/bin/bash

set -e

# Input and output directories
CONTRACTS_DIR="/contracts"
OUTPUT_DIR="/contracts/bundled_contracts"
BUNDLER="/qan-scripts/bundler"
MODULES_PATH="/app/node_modules"

# Ensure output directory exists
mkdir -p $OUTPUT_DIR

# Iterate through all Solidity files in the contracts directory
for contract in $CONTRACTS_DIR/*.sol; do
    # Define output file path
    output_file="$OUTPUT_DIR/$(basename $contract)"

    # Run the bundler script
    python3 $BUNDLER/bundler.py "$contract" "$output_file" --node-modules-path $MODULES_PATH
    # echo "Bundled $(basename $contract) -> $output_file"
done

#echo "All contracts bundled successfully."

