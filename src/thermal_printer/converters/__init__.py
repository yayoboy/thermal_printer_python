"""
Converters Module
=================

Modulo per la conversione di immagini in formati supportati dalle stampanti.
"""

from .escpos import ESCPOSConverter, split_image

__all__ = ['ESCPOSConverter', 'split_image']
