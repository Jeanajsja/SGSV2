import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKSPACE = os.path.abspath(os.path.join(ROOT, ".."))

for entry in list(sys.path):
    if entry.startswith(os.path.join(WORKSPACE, "services")):
        sys.path.remove(entry)

for entry in [WORKSPACE, ROOT]:
    if entry not in sys.path:
        sys.path.insert(0, entry)
else:
    sys.path.insert(0, ROOT)
