#!/bin/sh
set -eu
# Installs only into this prototype's ignored .mirofish folder.
GL_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
command -v uv >/dev/null 2>&1 || { echo 'Install uv from https://docs.astral.sh/uv/getting-started/installation/ first.'; exit 1; }
command -v git >/dev/null 2>&1 || { echo 'Git is required.'; exit 1; }
mkdir -p "$GL_ROOT/.mirofish"
if [ ! -d "$GL_ROOT/.mirofish/repo/.git" ]; then
  git clone https://github.com/shayswrld/mirofish.git "$GL_ROOT/.mirofish/repo"
fi
git -C "$GL_ROOT/.mirofish/repo" checkout --detach 8d4eea4dfa981ecd23c3b385953b4085dfd9b6ca
uv venv --python 3.12 "$GL_ROOT/.mirofish/venv"
uv pip install --python "$GL_ROOT/.mirofish/venv/bin/python" -r "$GL_ROOT/requirements-mirofish.txt"
printf '%s\n' 'Engine installed. Start Ollama and pull qwen3-coder:30b.' 'The bundled research graph is ready. To rebuild: .mirofish/venv/bin/python graph_pipeline.py --repo .mirofish/repo --output .travel-graph' 'Start the demo: python3 server.py --port 8765'
