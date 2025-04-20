"""
Permite que imports antiguos como
    from config.database import ...
sigan funcionando, exponiendo product_service.config
como un alias de módulo top‑level 'config' (igual para 'methods').
"""

import importlib
import sys as _sys

# Alias 'config'  -> product_service.config
_sys.modules.setdefault(
    "config",
    importlib.import_module(__name__ + ".config")
)

# Alias 'methods' -> product_service.methods
_sys.modules.setdefault(
    "methods",
    importlib.import_module(__name__ + ".methods")
)

# Alias 'pb' -> product_service.pb
_sys.modules.setdefault(
    "pb",
    importlib.import_module(__name__ + ".pb")
)
