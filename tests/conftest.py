import os
import sys

# permet d'importer app.py et utils/ depuis le dossier tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
