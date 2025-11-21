#!/usr/bin/env python
"""
Main entry point for running the BMW Sales Reporting Pipeline.
"""
import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from pipeline.pipeline import main

if __name__ == "__main__":
    sys.exit(main())
