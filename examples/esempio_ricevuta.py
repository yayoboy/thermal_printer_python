#!/usr/bin/env python3
"""
Esempio: Stampa di una Ricevuta
================================

Questo script mostra come stampare una ricevuta usando un template HTML.

Per eseguire questo esempio:
1. Modifica la configurazione della stampante (riga 25-30)
2. Esegui: python esempio_ricevuta.py
"""

import sys
from pathlib import Path

# Aggiungi la cartella src al path per importare il modulo
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from thermal_printer import ThermalPrinter, PrinterConfig
from datetime import datetime


def main():
    """Funzione principale"""

    # ========================================
    # 1. CONFIGURAZIONE STAMPANTE
    # ========================================
    # Modifica questi valori in base alla tua stampante!

    config = PrinterConfig(
        # Tipo di stampante: 'network', 'serial', o 'usb'
        printer_type='network',

        # Indirizzo stampante:
        # - Network: 'IP:porta' (es: '192.168.1.100:9100')
        # - Serial: porta (es: 'COM3' o '/dev/ttyUSB0')
        # - USB: 'vendorID:productID' (es: '0x04b8:0x0e15')
        endpoint='192.168.1.100:9100',

        # Larghezza stampante in pixel
        # 384px = stampante 58mm
        # 576px = stampante 80mm
        printer_width=384,

        # Opzioni di stampa
        cut_paper=True,        # Taglia carta automaticamente
        lines_before=2,        # Righe vuote prima
        lines_after=3,         # Righe vuote dopo
        split_printing=False,  # Dividi immagini lunghe (non necessario per ricevute)
    )

    # ========================================
    # 2. DATI DELLA RICEVUTA
    # ========================================

    # Ottieni data e ora correnti
    now = datetime.now()

    # Dati da inserire nel template
    dati_ricevuta = {
        # Informazioni negozio
        'negozio': {
            'nome': 'Bar Centrale',
            'indirizzo': 'Via Roma 123, Milano',
            'telefono': '02-1234567',
            'piva': 'IT12345678901'
        },

        # Informazioni ricevuta
        'numero_ricevuta': '00042',
        'data': now.strftime('%d/%m/%Y'),
        'ora': now.strftime('%H:%M:%S'),
        'operatore': 'Mario Rossi',

        # Lista articoli acquistati
        'items': [
            {
                'nome': 'Caffè',
                'quantita': 2,
                'prezzo': '3.00',
                'note': None
            },
            {
                'nome': 'Cornetto',
                'quantita': 1,
                'prezzo': '1.20',
                'note': None
            },
            {
                'nome': 'Acqua Naturale',
                'quantita': 1,
                'prezzo': '1.50',
                'note': '50cl'
            },
            {
                'nome': 'Tramezzino',
                'quantita': 1,
                'prezzo': '3.50',
                'note': 'Prosciutto e formaggio'
            },
        ],

        # Totali
        'subtotale': '9.20',
        'sconto': '0.00',
        'iva_percentuale': '10',
        'iva': '0.92',
        'totale': '10.12',

        # Pagamento
        'metodo_pagamento': 'Contanti',
        'ricevuto': '20.00',
        'resto': '9.88',

        # Barcode (opzionale)
        'barcode': '0004220230615',

        # Sito web (opzionale)
        'sito_web': 'www.barcentrale.it'
    }

    # ========================================
    # 3. STAMPA
    # ========================================

    print("\n" + "="*50)
    print("📄 STAMPA RICEVUTA")
    print("="*50 + "\n")

    # Crea l'oggetto stampante
    # Usando 'with' la stampante si chiude automaticamente
    with ThermalPrinter(config) as printer:

        # Path del template HTML
        template_path = Path(__file__).parent / 'template_ricevuta.html'

        # Verifica che il template esista
        if not template_path.exists():
            print(f"❌ Errore: Template non trovato in {template_path}")
            return

        # Leggi il template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_html = f.read()

        # Stampa usando il template
        print("🖨️  Invio ricevuta alla stampante...\n")

        success = printer.print_template(
            template_string=template_html,
            data=dati_ricevuta
        )

        if success:
            print("\n" + "="*50)
            print("✅ RICEVUTA STAMPATA CON SUCCESSO!")
            print("="*50 + "\n")
        else:
            print("\n" + "="*50)
            print("❌ ERRORE DURANTE LA STAMPA")
            print("="*50 + "\n")
            print("Verifica:")
            print("- La stampante sia accesa")
            print("- L'indirizzo sia corretto")
            print("- La stampante sia collegata alla rete")


if __name__ == "__main__":
    main()
