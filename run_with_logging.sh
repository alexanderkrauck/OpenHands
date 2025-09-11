#!/bin/bash
# OpenHands CLI with full logging enabled

# Setup logging
export LOG_LEVEL=DEBUG
export DEBUG=true
export LOG_TO_FILE=true
export LOG_ALL_EVENTS=true
export DEBUG_RUNTIME=true
export LOG_JSON="${LOG_JSON:-true}"

# Create log directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_DIR="./logs/session_${TIMESTAMP}"
mkdir -p "$LOG_DIR"

echo "📝 Logging to: $LOG_DIR"
echo "🚀 Starting OpenHands with full logging..."

# Run OpenHands with all arguments passed through, tee to log file

openhands --log-level DEBUG "$@" 2>&1 | tee "$LOG_DIR/full.log"