"""
parse_instruction_adapter.py -- imports your EXISTING src/parse_instruction.py
so the web backend reuses the exact same Gemini logic you already
built and tested, instead of duplicating it.
"""
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from parse_instruction import parse_instruction  # noqa: E402, F401