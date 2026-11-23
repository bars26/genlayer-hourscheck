"""Shared helpers for the direct-mode tests."""

import json
import os

BRADBURY = os.environ.get("HOURSCHECK_NETWORK") == "bradbury"
if BRADBURY:
    os.environ.setdefault("GENVM_VERSION", "v0.6.0-rc10")

CONTRACT_PATH = "contracts/hours_check.bradbury.py" if BRADBURY else "contracts/hours_check.py"


def llm_json(obj):
    """An LLM mock answering JSON (bytes on the Bradbury harness, which otherwise turns string mocks into dicts)."""
    text = json.dumps(obj)
    return text.encode() if BRADBURY else text
