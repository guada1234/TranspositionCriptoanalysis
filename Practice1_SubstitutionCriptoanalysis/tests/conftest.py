"""
Makes 'import basics', 'import caesar', etc. work when pytest is run
from the project root, no matter which folder pytest is launched from.
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)