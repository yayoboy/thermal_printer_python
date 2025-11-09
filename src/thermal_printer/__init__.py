"""
Thermal Printer Python Library
===============================

Una libreria Python per stampare contenuti HTML/CSS su stampanti termiche.

Caratteristiche principali:
- Templating con Jinja2 (simile a Nunjucks)
- Rendering HTML -> Immagine con Selenium
- Conversione Immagine -> Comandi ESC/POS
- Supporto per stampanti USB, Seriali e Network

Esempio d'uso:
    >>> from thermal_printer import ThermalPrinter
    >>> printer = ThermalPrinter(printer_type='network', endpoint='192.168.1.100:9100')
    >>> printer.print_template('template.html', {'name': 'Mario', 'age': 30})
"""

from .printer import ThermalPrinter
from .config import PrinterConfig

__version__ = "1.0.0"
__author__ = "Thermal Printer Python"

__all__ = ["ThermalPrinter", "PrinterConfig"]
