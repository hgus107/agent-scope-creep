"""Run log. One JSONL file per run; every event carries the tool-call index."""
import json
import time
from pathlib import Path


class RunLog:
    def __init__(self, path: Path, run_id: str, arm: str, model: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")
        self.call_index = 0
        self.event("run_start", run_id=run_id, arm=arm, model=model)

    def event(self, kind: str, **fields):
        rec = {
            "ts": time.time(),
            "call_index": self.call_index,
            "event": kind,
            **fields,
        }
        self._fh.write(json.dumps(rec) + "\n")
        self._fh.flush()
        return rec

    def close(self, **fields):
        self.event("run_end", **fields)
        self._fh.close()
