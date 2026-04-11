#!/bin/bash
# MemPalace MCP server wrapper for Claude Code
# Registered via: claude mcp add mempalace -- /path/to/this/script
set -e
PYTHON=/Users/lexa/Desktop/lexa/omega/omega-ancient-texts-analysis/.venv/bin/python3
PALACE=/Users/lexa/Desktop/lexa/omega/omega-palace
exec "$PYTHON" -m mempalace.mcp_server --palace "$PALACE"
