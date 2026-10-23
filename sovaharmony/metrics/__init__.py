# metrics/__init__.py
import os
import glob

# Importar todos los archivos Python en la carpeta
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]

# Importa cada módulo dinámicamente
for module in __all__:
    exec(f"from .{module} import *")
