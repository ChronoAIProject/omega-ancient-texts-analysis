import json
import time
import os
import fcntl
import datetime
from pathlib import Path
from typing import Any

try:
    import anthropic
except ImportError:
    anthropic = None


REPO_ROOT = Path(__file__).parent.parent
DISPATCH_LOG = REPO_ROOT / "workspace" / "dispatch_log.jsonl"
PRICING_AS_OF = "2026-04-16"
PRICING_USD_PER_MTOK = {
    "claude-opus-4-6": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
}


class ClaudeDispatchError(Exception):
    pass


def _compute_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    rates = PRICING_USD_PER_MTOK.get(model)
    if rates is None:
        print(
            f"warning: no pricing configured for {model!r} as of {PRICING_AS_OF}",
            file=os.sys.stderr,
        )
        return 0.0
    return (tokens_in / 1_000_000) * rates["input"] + (tokens_out / 1_000_000) * rates["output"]


def _append_log(entry: dict) -> None:
    try:
        DISPATCH_LOG.parent.mkdir(parents=True, exist_ok=True)
        with DISPATCH_LOG.open("a", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                handle.write(json.dumps(entry) + "\n")
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except Exception as exc:
        print(f"warning: failed to append dispatch log: {exc}", file=os.sys.stderr)


def dispatch(
    system: str,
    user: str,
    tool_name: str,
    input_schema: dict,
    *,
    model: str = "claude-opus-4-6",
    max_tokens: int = 4096,
    gate: str = "unknown",
    item_id: str = "unknown",
    mock: bool | None = None,
) -> dict:
    if mock is None:
        mock = os.environ.get("MOCK_CLAUDE") == "1"

    t0 = time.monotonic()
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if mock:
        result = {"mock": True, "gate": gate, "item_id": item_id}
        _append_log(
            {
                "ts": ts,
                "dispatcher": "claude",
                "gate": gate,
                "item_id": item_id,
                "model": model,
                "tool_name": tool_name,
                "tokens_in": 0,
                "tokens_out": 0,
                "latency_ms": int((time.monotonic() - t0) * 1000),
                "cost_usd": 0.0,
                "mock": True,
                "success": True,
            }
        )
        return result

    if anthropic is None:
        raise ClaudeDispatchError("anthropic SDK not installed — run: pip install anthropic")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise ClaudeDispatchError("ANTHROPIC_API_KEY not set in environment")

    client = anthropic.Anthropic()
    response: Any | None = None

    for attempt in range(3):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
                tools=[
                    {
                        "name": tool_name,
                        "description": f"Return structured {tool_name} result.",
                        "input_schema": input_schema,
                    }
                ],
                tool_choice={"type": "tool", "name": tool_name},
            )
        except (anthropic.RateLimitError, anthropic.APIConnectionError) as exc:
            if attempt < 2:
                time.sleep(2**attempt)
                continue
            _append_log(
                {
                    "ts": ts,
                    "dispatcher": "claude",
                    "gate": gate,
                    "item_id": item_id,
                    "model": model,
                    "tool_name": tool_name,
                    "tokens_in": 0,
                    "tokens_out": 0,
                    "latency_ms": int((time.monotonic() - t0) * 1000),
                    "cost_usd": 0.0,
                    "mock": False,
                    "success": False,
                    "error": str(exc),
                }
            )
            raise ClaudeDispatchError(str(exc)) from exc
        except anthropic.APIStatusError as exc:
            if getattr(exc, "status_code", 0) >= 500 and attempt < 2:
                time.sleep(2**attempt)
                continue
            _append_log(
                {
                    "ts": ts,
                    "dispatcher": "claude",
                    "gate": gate,
                    "item_id": item_id,
                    "model": model,
                    "tool_name": tool_name,
                    "tokens_in": 0,
                    "tokens_out": 0,
                    "latency_ms": int((time.monotonic() - t0) * 1000),
                    "cost_usd": 0.0,
                    "mock": False,
                    "success": False,
                    "error": str(exc),
                }
            )
            raise ClaudeDispatchError(str(exc)) from exc
        except Exception as exc:
            _append_log(
                {
                    "ts": ts,
                    "dispatcher": "claude",
                    "gate": gate,
                    "item_id": item_id,
                    "model": model,
                    "tool_name": tool_name,
                    "tokens_in": 0,
                    "tokens_out": 0,
                    "latency_ms": int((time.monotonic() - t0) * 1000),
                    "cost_usd": 0.0,
                    "mock": False,
                    "success": False,
                    "error": str(exc),
                }
            )
            raise ClaudeDispatchError(str(exc)) from exc
        break

    if response is None:
        raise ClaudeDispatchError("dispatch failed without a response")

    tokens_in = response.usage.input_tokens
    tokens_out = response.usage.output_tokens
    cost_usd = _compute_cost(model, tokens_in, tokens_out)

    result: dict[str, Any] | None = None
    for block in response.content:
        if block.type == "tool_use" and block.name == tool_name:
            result = block.input
            break

    if result is None:
        _append_log(
            {
                "ts": ts,
                "dispatcher": "claude",
                "gate": gate,
                "item_id": item_id,
                "model": model,
                "tool_name": tool_name,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "latency_ms": int((time.monotonic() - t0) * 1000),
                "cost_usd": cost_usd,
                "mock": False,
                "success": False,
                "error": "no tool_use block in response",
            }
        )
        raise ClaudeDispatchError("no tool_use block in response")

    _append_log(
        {
            "ts": ts,
            "dispatcher": "claude",
            "gate": gate,
            "item_id": item_id,
            "model": model,
            "tool_name": tool_name,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "latency_ms": int((time.monotonic() - t0) * 1000),
            "cost_usd": cost_usd,
            "mock": False,
            "success": True,
        }
    )
    return result


if __name__ == "__main__":
    os.environ["MOCK_CLAUDE"] = "1"
    demo_result = dispatch(
        system="Return a structured publication verdict.",
        user="Decide whether the demo should pass.",
        tool_name="publication_verdict",
        input_schema={
            "type": "object",
            "properties": {"verdict": {"type": "string"}},
            "required": ["verdict"],
        },
        gate="demo",
        item_id="demo-item",
        mock=True,
    )
    print(demo_result)
    print(f"log entry appended to {DISPATCH_LOG}")
