#!/usr/bin/env bash
set -euo pipefail

# Build the React frontend and verify output.
# Run from repo root.

cd "$(dirname "$0")"

echo "Installing frontend dependencies..."
cd frontend
npm install

echo "Building frontend..."
npm run build

echo "Done. Built files are in frontend/dist/."
