#!/bin/bash

# Loop through all .txt files safely
find . -type f -name "*.txt" | while read -r file; do
    
    # Step 1: Extract category
    category=$(grep -m 1 "^category:" "$file" | cut -d' ' -f2- | tr -d '\r')

    # Step 2: Skip if no category found
    if [ -z "$category" ]; then
        echo "Skipping $file (no category)"
        continue
    fi

    # Step 3: Create category directory
    mkdir -p "$category"

    # Step 4: Remove leading ./ from path
    relpath=$(echo "$file" | sed 's|^./||')

    # Step 5: Convert path to dashed format
    newname=$(echo "$relpath" | tr '/' '-')

    # Step 6: Move file
    mv "$file" "$category/$newname"

done

# Step 7: Delete empty directories
find . -type d -empty -delete

# Step 8: Generate hash
find . -type f | LC_ALL=C sort | sha256sum
