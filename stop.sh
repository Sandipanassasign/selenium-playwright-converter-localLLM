#!/bin/bash
# stop.sh

echo "🛑 Stopping Converter Server..."

# Find PID running on port 8000
PID=$(lsof -t -i:8000)

if [ -z "$PID" ]; then
    echo "✅ No server running on port 8000."
else
    kill -9 $PID
    echo "✅ Server (PID $PID) stopped."
fi
