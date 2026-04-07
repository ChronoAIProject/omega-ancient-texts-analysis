#!/usr/bin/env python3
"""Content publishing scheduler.

Dispatches generated content to social networks via:
1. Direct platform APIs (Twitter, LinkedIn, YouTube)
2. n8n webhook integration (for Ada's workflows)
"""

import json
import urllib.request
from datetime import datetime


class Publisher:
    """Multi-platform content publisher."""

    def __init__(self, config: dict):
        self.config = config
        self.platforms = {p["name"]: p for p in config.get("publish", {}).get("platforms", [])}
        self.n8n_config = config.get("n8n", {})

    def publish_via_n8n(self, content: dict) -> dict:
        """Send content to n8n webhook for automated publishing."""
        webhook_url = f"{self.n8n_config['base_url']}{self.n8n_config['webhook_path']}"
        payload = json.dumps({
            "source": "omega-ancient-texts",
            "timestamp": datetime.now().isoformat(),
            "content": content,
        }).encode()

        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {"status": "sent", "code": resp.status}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def publish_to_platform(self, platform: str, content: dict) -> dict:
        """Publish to a specific platform."""
        if platform not in self.platforms:
            return {"status": "error", "error": f"Unknown platform: {platform}"}
        if not self.platforms[platform].get("enabled"):
            return {"status": "skipped", "reason": "disabled"}

        # TODO: Implement per-platform API calls
        # For now, delegate to n8n
        return self.publish_via_n8n({
            "platform": platform,
            **content,
        })

    def publish_all(self, content: dict) -> dict:
        """Publish to all enabled platforms."""
        results = {}
        for name, cfg in self.platforms.items():
            if cfg.get("enabled"):
                results[name] = self.publish_to_platform(name, content)
        return results
