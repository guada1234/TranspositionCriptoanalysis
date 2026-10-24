# Permite importar los módulos de la carpeta principal desde tests/
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))