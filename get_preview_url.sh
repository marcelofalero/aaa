#!/bin/bash

# Configuration
PROJECT_NAME="aaa"

# Detect current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Get the latest deployment URL for the current branch
PREVIEW_URL=$(wrangler pages deployment list --project-name "$PROJECT_NAME" | grep "│.*│.* $BRANCH " | head -n 1 | awk -F'│' '{print $6}' | xargs)

if [ -z "$PREVIEW_URL" ]; then
    echo "Error: Could not find a deployment for branch '$BRANCH'."
    exit 1
fi

echo "$PREVIEW_URL"
