#!/bin/bash
# 自动轮询 NotebookLM artifacts → 下载 → 上传 GitHub release
# Usage: bash tools/sync_artifacts.sh [--once]
# 默认每 60 秒轮询一次，--once 只跑一次

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
VENV="$ROOT/.venv/bin/python3"
REPO="the-omega-institute/Omega-paper-series"
TAG="cultural-media-v1"

cd "$ROOT"

download_and_upload() {
    echo "[$(date +%H:%M:%S)] Checking for new artifacts..."

    # Download from NotebookLM
    $VENV -c "
import asyncio
from pathlib import Path
from notebooklm import NotebookLMClient
ARTIFACTS = Path('workspace/artifacts')
async def dl():
    async with await NotebookLMClient.from_storage() as c:
        count = 0
        for nb in await c.notebooks.list():
            if not nb.title.startswith('Omega:'): continue
            slug = nb.title.replace('Omega: ', '')
            out = ARTIFACTS / slug; out.mkdir(parents=True, exist_ok=True)
            for kind, ext, dl_fn in [
                ('list_video', '_video.mp4', c.artifacts.download_video),
                ('list_slide_decks', '_slides.pdf', c.artifacts.download_slide_deck),
                ('list_infographics', '_infographic.png', c.artifacts.download_infographic),
            ]:
                f = out / f'{slug}{ext}'
                if f.exists(): continue
                try:
                    items = await getattr(c.artifacts, kind)(nb.id)
                    if items:
                        await dl_fn(nb.id, str(f))
                        print(f'  ✓ {slug}{ext} ({f.stat().st_size // 1024}KB)')
                        count += 1
                except: pass
        print(f'  Downloaded: {count} new')
asyncio.run(dl())
" 2>&1

    # Upload to GitHub release
    echo "  Uploading to release..."
    python3 tools/upload_to_github_release.py 2>&1 | grep -E "✓|Uploaded"

    echo "[$(date +%H:%M:%S)] Sync complete."
}

if [ "$1" = "--once" ]; then
    download_and_upload
else
    echo "Polling every 60s. Ctrl+C to stop."
    while true; do
        download_and_upload
        echo "  Waiting 60s..."
        sleep 60
    done
fi
