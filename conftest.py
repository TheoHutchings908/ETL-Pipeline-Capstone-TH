# conftest.py
import sys, os

# compute the absolute path to ./src
SRC = os.path.join(os.path.dirname(__file__), "src")

# insert it at the front of sys.path:
sys.path.insert(0, os.path.abspath(SRC))
