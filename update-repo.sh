#!/bin/bash

# Check if the script is running in a Git repository directory
if [ ! -d ".git" ]; then
    echo "Error: This script must be run in a Git repository directory."
    exit 1
fi

# Commit message
COMMIT_MESSAGE=${1:-"Update files: $(date +'%Y-%m-%d %H:%M:%S')"}

# Add all changes to the index
git add .

# Check for changes to commit
if git diff-index --quiet HEAD --; then
    echo "No changes to commit."
    exit 0
fi

# Create a commit
echo "Creating a commit with the message: \"$COMMIT_MESSAGE\""
git commit -m "$COMMIT_MESSAGE"

# Pull the latest changes from the remote repository
echo "Pulling latest changes from the remote repository..."
git pull origin main --rebase

if [ $? -ne 0 ]; then
    echo "Error while pulling changes. Resolve conflicts and try again."
    exit 1
fi

# Push the changes
echo "Pushing changes to the remote repository..."
git push origin main

# Success message
if [ $? -eq 0 ]; then
    echo "Changes successfully pushed to the remote repository."
else
    echo "Error while pushing changes. Check your Git settings."
    exit 1
fi
