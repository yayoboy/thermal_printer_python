"""
Templates Module
================

Modulo per la gestione del templating e rendering HTML.
"""

from .template_engine import TemplateEngine, create_complete_html
from .renderer import HTMLRenderer

__all__ = ['TemplateEngine', 'create_complete_html', 'HTMLRenderer']
