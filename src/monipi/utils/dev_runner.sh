

#!/bin/bash

# RUN WITH
# ./src/monipi/utils/dev_runner.sh

# Resolve project root relative to this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../" && pwd)"

cd "$PROJECT_ROOT"

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
  if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
  else
    echo "No .venv found. Please activate your environment manually."
  fi
fi

# Start main sampler in background
echo "Starting sampler..."
python3 -m monipi &
SAMPLER_PID=$!

# Start Flask app
echo "Starting web app..."
python3 -m monipi.web.app &
WEB_PID=$!

# Handle shutdown (Ctrl+C)
trap "echo 'Stopping...'; kill $SAMPLER_PID $WEB_PID" SIGINT

# Wait for both processes
wait