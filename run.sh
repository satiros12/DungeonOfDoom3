#!/bin/bash
# Escape the Dungeon of Doom - Launch Script
# This script runs the game using UV (Python package manager)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ESCAPE THE DUNGEON OF DOOM${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: UV is not installed${NC}"
    echo "Please install UV first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Or use pip:"
    echo "  pip install uv"
    exit 1
fi

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python is not installed${NC}"
    exit 1
fi

echo -e "${YELLOW}Starting game...${NC}"
echo ""

# Run the game
uv run python -m src.main "$@"

# Exit message
echo ""
echo -e "${GREEN}Thanks for playing Escape the Dungeon of Doom!${NC}"
