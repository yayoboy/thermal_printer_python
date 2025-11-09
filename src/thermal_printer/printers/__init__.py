"""
Backend di Stampa
==================

Questo modulo contiene i diversi backend per comunicare con le stampanti termiche.

Backend disponibili:
- NetworkPrinter: Stampa via rete TCP/IP
- SerialPrinter: Stampa via porta seriale
- USBPrinter: Stampa via USB raw
"""

from .network import NetworkPrinter
from .serial_printer import SerialPrinter
from .usb import USBPrinter

__all__ = ['NetworkPrinter', 'SerialPrinter', 'USBPrinter']
