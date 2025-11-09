"""
Configurazione della Stampante Termica
======================================

Questo file contiene le impostazioni per configurare la stampante termica.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PrinterConfig:
    """
    Configurazione della stampante termica.

    Questa classe contiene tutte le impostazioni necessarie per configurare
    come la stampante deve funzionare.

    Attributi:
        printer_type (str): Tipo di stampante da usare.
            Opzioni: 'usb', 'serial', 'network'

        endpoint (str): Indirizzo della stampante.
            - Per USB: vendorID:productID (es: '0x04b8:0x0e15')
            - Per Serial: porta seriale (es: 'COM3' o '/dev/ttyUSB0')
            - Per Network: IP:porta (es: '192.168.1.100:9100')

        printer_width (int): Larghezza della stampante in pixel.
            Valori comuni:
            - 384px per stampanti da 58mm
            - 576px per stampanti da 80mm

        cut_paper (bool): Se True, taglia automaticamente la carta dopo la stampa

        lines_before (int): Numero di righe vuote da stampare prima del contenuto

        lines_after (int): Numero di righe vuote da stampare dopo il contenuto

        split_printing (bool): Se True, divide immagini lunghe in chunk più piccoli

        split_height (int): Altezza massima (in pixel) per ogni chunk quando split_printing è True

        split_delay (float): Delay in secondi tra un chunk e l'altro

        use_esc_star (bool): Se True, usa il comando ESC * invece di GS v 0
            ESC * è più compatibile con stampanti vecchie
    """

    # Tipo di stampante: 'usb', 'serial', 'network'
    printer_type: str = 'network'

    # Indirizzo/endpoint della stampante
    endpoint: str = '192.168.1.100:9100'

    # Larghezza della stampante in pixel (384 per 58mm, 576 per 80mm)
    printer_width: int = 384

    # Se True, taglia la carta automaticamente dopo la stampa
    cut_paper: bool = True

    # Numero di righe vuote prima del contenuto
    lines_before: int = 2

    # Numero di righe vuote dopo il contenuto
    lines_after: int = 3

    # Se True, divide immagini lunghe in più parti
    split_printing: bool = True

    # Altezza massima di ogni parte (in pixel)
    split_height: int = 1000

    # Delay tra una parte e l'altra (in secondi)
    split_delay: float = 0.1

    # Se True, usa ESC * invece di GS v 0 (più compatibile)
    use_esc_star: bool = False

    def validate(self) -> bool:
        """
        Verifica che la configurazione sia valida.

        Returns:
            bool: True se la configurazione è valida, False altrimenti
        """
        # Verifica che il tipo di stampante sia valido
        if self.printer_type not in ['usb', 'serial', 'network']:
            print(f"❌ Errore: printer_type deve essere 'usb', 'serial' o 'network', non '{self.printer_type}'")
            return False

        # Verifica che la larghezza sia ragionevole
        if self.printer_width < 100 or self.printer_width > 1000:
            print(f"❌ Errore: printer_width deve essere tra 100 e 1000 pixel, non {self.printer_width}")
            return False

        # Verifica che l'endpoint sia specificato
        if not self.endpoint or self.endpoint.strip() == '':
            print(f"❌ Errore: endpoint non può essere vuoto")
            return False

        # Tutto ok!
        return True

    def __str__(self) -> str:
        """
        Rappresentazione testuale della configurazione.

        Returns:
            str: Descrizione della configurazione
        """
        return f"""
Configurazione Stampante Termica:
  Tipo: {self.printer_type}
  Endpoint: {self.endpoint}
  Larghezza: {self.printer_width}px
  Taglia carta: {'Sì' if self.cut_paper else 'No'}
  Righe prima: {self.lines_before}
  Righe dopo: {self.lines_after}
  Split printing: {'Sì' if self.split_printing else 'No'}
    - Altezza chunk: {self.split_height}px
    - Delay: {self.split_delay}s
  Usa ESC*: {'Sì' if self.use_esc_star else 'No'}
"""


# Configurazioni predefinite per stampanti comuni
PRESETS = {
    # Stampante termica da 58mm
    '58mm': PrinterConfig(
        printer_width=384,
        split_height=800,
    ),

    # Stampante termica da 80mm
    '80mm': PrinterConfig(
        printer_width=576,
        split_height=1000,
    ),
}


def get_preset(preset_name: str) -> Optional[PrinterConfig]:
    """
    Ottiene una configurazione predefinita.

    Args:
        preset_name (str): Nome del preset ('58mm' o '80mm')

    Returns:
        PrinterConfig: Configurazione predefinita, o None se non trovata

    Esempio:
        >>> config = get_preset('58mm')
        >>> config.printer_width
        384
    """
    return PRESETS.get(preset_name)
