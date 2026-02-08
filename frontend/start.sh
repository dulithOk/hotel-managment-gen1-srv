#!/bin/bash

echo "Starting Hotel Admin Frontend..."
echo "================================"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start development server
echo "Starting Next.js development server on http://localhost:3000"
echo "================================"
npm run dev
