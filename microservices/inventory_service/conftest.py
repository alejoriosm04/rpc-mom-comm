# microservices/inventory_service/conftest.py
import sys
from pathlib import Path

MICROSERVICES_DIR = Path(__file__).resolve().parent.parent  
if str(MICROSERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(MICROSERVICES_DIR))

