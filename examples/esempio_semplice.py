#!/usr/bin/env python3
"""
Esempio Semplice: Stampa Testo
===============================

Questo è l'esempio più semplice per iniziare.
Stampa solo testo senza template complicati.

Per eseguire:
python esempio_semplice.py
"""

import sys
from pathlib import Path

# Aggiungi la cartella src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from thermal_printer import ThermalPrinter, PrinterConfig


def main():
    """Funzione principale"""

    print("\n🖨️  ESEMPIO SEMPLICE - STAMPA TESTO\n")

    # ========================================
    # CONFIGURAZIONE (MODIFICARE QUI!)
    # ========================================

    config = PrinterConfig(
        printer_type='network',              # Tipo: 'network', 'serial', 'usb'
        endpoint='192.168.1.100:9100',       # Indirizzo stampante
        printer_width=384,                   # Larghezza (384=58mm, 576=80mm)
        cut_paper=True                       # Taglia carta alla fine
    )

    # ========================================
    # STAMPA
    # ========================================

    # Crea stampante
    with ThermalPrinter(config) as printer:

        # Esempio 1: Testo semplice
        print("📝 Stampa 1: Testo semplice\n")
        printer.print_text("Ciao Mondo!", font_size=16, center=True)

        # Avanza carta per separare le stampe
        printer.feed_paper(3)

        # Esempio 2: Testo formattato
        print("📝 Stampa 2: Testo formattato\n")
        printer.print_text("TITOLO GRANDE", font_size=20, bold=True, center=True)
        printer.print_text("Sottotitolo piccolo", font_size=10, center=True)

        # Avanza carta
        printer.feed_paper(3)

        # Esempio 3: Stampa con template HTML semplice
        print("📝 Stampa 3: Template HTML\n")

        template_html = """
        <div style="padding: 10px;">
            <h1 style="text-align: center; font-size: 18px;">
                {{ titolo }}
            </h1>
            <p style="text-align: center; font-size: 12px;">
                {{ sottotitolo }}
            </p>
            <hr style="margin: 10px 0; border: 1px solid black;">
            <p style="font-size: 11px;">
                {{ messaggio }}
            </p>
        </div>
        """

        dati = {
            'titolo': 'Thermal Printer Python',
            'sottotitolo': 'Esempio di stampa',
            'messaggio': 'Questo è un esempio di come stampare contenuti personalizzati usando template HTML con dati dinamici.'
        }

        printer.print_template(template_html, dati)

    print("\n✅ Stampa completata!\n")


if __name__ == "__main__":
    main()
