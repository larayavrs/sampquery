#!/bin/bash

cd "$(dirname "$0")/examples" || exit 1

for file in *.py; do
    echo "Executing $file..."
    python "$file"
    if [ $? -ne 0 ]; then
        echo "Wrong output in $file"
        exit 1
    fi
done

echo "All examples were executed successfully"