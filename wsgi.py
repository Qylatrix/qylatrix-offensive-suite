import sys
import os

# ── PythonAnywhere WSGI entry point ──────────────────────────────
# Replace 'qylatrix' below with your actual PythonAnywhere username
project_home = '/home/qylatrix/qylatrix-offensive-suite'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from webapp import app as application  # noqa
