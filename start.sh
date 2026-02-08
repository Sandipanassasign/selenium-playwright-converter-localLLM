#!/bin/bash
# start.sh

# 1. Create Virtual Environment if not exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

# 2. Activate Virtual Environment
source .venv/bin/activate

# 3. Install Dependencies
echo "📦 Installing Python dependencies in venv..."
pip install fastapi uvicorn requests

# 4. Check if install succeeded
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check network or permissions."
    exit 1
fi

# 5. Start Server
echo "🚀 Starting Server on http://localhost:8000..."
python3 server.py
