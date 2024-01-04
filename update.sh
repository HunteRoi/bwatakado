#!/bin/bash

echo "Updating the application..."

# Pull the latest changes
if [ -d ".git" ]; then
  git pull
else
  echo "Git directory does not exist. Please clone the repository."
  exit 1
fi

echo "Update complete, running startup script..."

./install.sh
