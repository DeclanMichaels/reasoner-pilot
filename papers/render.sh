#!/usr/bin/env bash
#
# Render a paper from Markdown to PDF via HTML + WeasyPrint. Recipe from rcp-experiment/papers.
# Creates a virtual environment, installs dependencies, and runs the renderer.
#
# Usage:
#   papers/render.sh papers/inlanguage-mfq2-DRAFT.md
#   ./render.sh --clean

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.render-venv"

# --- Handle --clean ---
if [[ "${1:-}" == "--clean" ]]; then
    echo "Removing virtual environment..."
    rm -rf "$VENV_DIR"
    echo "Done."
    exit 0
fi

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <markdown-file>"
    echo "       $0 --clean"
    exit 1
fi

# --- Ensure venv exists ---
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "Installing dependencies..."
    "$VENV_DIR/bin/pip" install --quiet --upgrade pip
    "$VENV_DIR/bin/pip" install --quiet markdown weasyprint
    echo "Environment ready."
fi

# --- Render ---
exec "$VENV_DIR/bin/python" "$SCRIPT_DIR/render_html_pdf.py" "$1"
