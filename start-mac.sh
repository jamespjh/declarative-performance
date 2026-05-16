#!/usr/bin/env bash
# Bootstrap script for macOS: install Carla and other Homebrew dependencies
# Usage: ./start-mac.sh

set -euo pipefail

# Check for Homebrew
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Please install Homebrew first: https://brew.sh/"
  exit 1
fi

# Install Carla (audio plugin host)
echo "Installing Carla..."
brew install carla

# Add other dependencies below as needed
echo "Installing other dependencies..."
# brew install <dependency>
# brew install <another-dependency>

echo "All dependencies installed."
