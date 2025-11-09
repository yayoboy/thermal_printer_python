"""
Classe Principale ThermalPrinter
=================================

Questa è la classe principale che mette insieme tutti i componenti:
- Templating (Jinja2)
- Rendering (HTML -> Immagine)
- Conversione (Immagine -> ESC/POS)
- Stampa (Network/Serial/USB)
"""

from PIL import Image
from typing import Dict, Any, Optional, List
from pathlib import Path

from .config import PrinterConfig
from .templates.template_engine import TemplateEngine, create_complete_html
from .templates.renderer import HTMLRenderer
from .converters.escpos import ESCPOSConverter, split_image
from .printers.network import NetworkPrinter
from .printers.serial_printer import SerialPrinter
from .printers.usb import USBPrinter


class ThermalPrinter:
    """
    Classe principale per gestire la stampa su stampanti termiche.

    Questa classe combina tutti i componenti del sistema:
    1. Carica e renderizza template HTML con Jinja2
    2. Converte HTML in immagine usando un browser headless
    3. Converte l'immagine in comandi ESC/POS
    4. Invia i comandi alla stampante (network/serial/USB)

    Esempio d'uso completo:
        >>> # Crea configurazione
        >>> from thermal_printer import ThermalPrinter, PrinterConfig
        >>>
        >>> config = PrinterConfig(
        ...     printer_type='network',
        ...     endpoint='192.168.1.100:9100',
        ...     printer_width=384
        ... )
        >>>
        >>> # Crea stampante
        >>> printer = ThermalPrinter(config)
        >>>
        >>> # Stampa da template
        >>> printer.print_template(
        ...     template_string='<h1>Ciao {{ nome }}!</h1>',
        ...     data={'nome': 'Mario'}
        ... )
        >>>
        >>> # Oppure stampa un'immagine esistente
        >>> img = Image.open('logo.png')
        >>> printer.print_image(img)
    """

    def __init__(
        self,
        config: Optional[PrinterConfig] = None,
        templates_dir: Optional[str] = None
    ):
        """
        Inizializza la stampante termica.

        Args:
            config (PrinterConfig, opzionale): Configurazione della stampante.
                Se None, usa configurazione di default.

            templates_dir (str, opzionale): Cartella dove cercare i template.
                Se specificato, potrai caricare template da file.
        """
        # Se non fornita configurazione, usa quella di default
        if config is None:
            config = PrinterConfig()

        # Valida la configurazione
        if not config.validate():
            raise ValueError("Configurazione stampante non valida")

        self.config = config

        # Inizializza i componenti
        print(f"🚀 Inizializzazione ThermalPrinter")
        print(f"   Tipo: {config.printer_type}")
        print(f"   Endpoint: {config.endpoint}")
        print(f"   Larghezza: {config.printer_width}px")

        # 1. Template Engine (Jinja2)
        self.template_engine = TemplateEngine(templates_dir)

        # 2. HTML Renderer (html2image o selenium)
        self.renderer = None  # Inizializzato on-demand

        # 3. ESC/POS Converter
        self.converter = ESCPOSConverter(use_esc_star=config.use_esc_star)

        # 4. Printer Backend
        self.printer_backend = self._create_printer_backend()

        print(f"✅ ThermalPrinter inizializzato\n")

    def _create_printer_backend(self):
        """
        Crea il backend di stampa appropriato in base alla configurazione.

        Returns:
            NetworkPrinter, SerialPrinter, o USBPrinter
        """
        if self.config.printer_type == 'network':
            # Parse endpoint "IP:porta"
            parts = self.config.endpoint.split(':')
            host = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 9100
            return NetworkPrinter(host, port)

        elif self.config.printer_type == 'serial':
            # Endpoint è la porta seriale (es: 'COM3' o '/dev/ttyUSB0')
            return SerialPrinter(self.config.endpoint)

        elif self.config.printer_type == 'usb':
            # Parse endpoint "vendorID:productID"
            parts = self.config.endpoint.split(':')
            vendor_id = int(parts[0], 16)  # Converti da hex
            product_id = int(parts[1], 16)
            return USBPrinter(vendor_id, product_id)

        else:
            raise ValueError(f"Tipo stampante '{self.config.printer_type}' non supportato")

    def _get_renderer(self) -> HTMLRenderer:
        """
        Ottiene il renderer HTML (lazy initialization).

        Returns:
            HTMLRenderer: Renderer HTML inizializzato
        """
        if self.renderer is None:
            self.renderer = HTMLRenderer(
                width=self.config.printer_width,
                method='html2image'  # Puoi cambiare in 'selenium' se preferisci
            )
        return self.renderer

    def print_template(
        self,
        template_string: str,
        data: Dict[str, Any],
        template_file: Optional[str] = None
    ) -> bool:
        """
        Stampa un template HTML con dati.

        Questo è il metodo principale per stampare contenuti personalizzati.

        Args:
            template_string (str): Template HTML come stringa.
                Usa None se vuoi caricare da file.

            data (dict): Dizionario con i dati da inserire nel template.
                Le chiavi del dizionario sono accessibili nel template.

            template_file (str, opzionale): Nome del file template da caricare.
                Usa questo invece di template_string per caricare da file.

        Returns:
            bool: True se la stampa è riuscita, False altrimenti

        Esempio:
            >>> # Da stringa
            >>> printer.print_template(
            ...     template_string='<h1>{{ titolo }}</h1><p>{{ testo }}</p>',
            ...     data={'titolo': 'Ricevuta', 'testo': 'Totale: €19.99'}
            ... )
            True
            >>>
            >>> # Da file
            >>> printer.print_template(
            ...     template_file='ricevuta.html',
            ...     data={'items': [...], 'totale': 19.99}
            ... )
            True
        """
        try:
            print("📄 Rendering template...")

            # 1. Renderizza il template con Jinja2
            if template_file:
                # Carica da file
                body_html = self.template_engine.render_file(template_file, data)
            else:
                # Renderizza da stringa
                body_html = self.template_engine.render_string(template_string, data)

            # 2. Crea HTML completo (con DOCTYPE, head, body)
            full_html = create_complete_html(body_html, self.config.printer_width)

            # 3. Renderizza HTML -> Immagine
            print("🖼️  Rendering HTML -> Immagine...")
            renderer = self._get_renderer()
            image = renderer.render_html(full_html)

            # 4. Stampa l'immagine
            return self.print_image(image)

        except Exception as e:
            print(f"❌ Errore durante la stampa del template: {e}")
            import traceback
            traceback.print_exc()
            return False

    def print_image(self, image: Image.Image) -> bool:
        """
        Stampa un'immagine PIL.

        Args:
            image (PIL.Image.Image): Immagine da stampare

        Returns:
            bool: True se la stampa è riuscita, False altrimenti

        Esempio:
            >>> from PIL import Image
            >>> img = Image.open('logo.png')
            >>> printer.print_image(img)
            True
        """
        try:
            # 1. Ridimensiona se necessario per fittare la larghezza stampante
            if image.size[0] != self.config.printer_width:
                print(f"📏 Ridimensionamento immagine a {self.config.printer_width}px...")
                aspect_ratio = image.size[1] / image.size[0]
                new_height = int(self.config.printer_width * aspect_ratio)
                image = image.resize((self.config.printer_width, new_height), Image.Resampling.LANCZOS)

            # 2. Split se necessario
            if self.config.split_printing:
                images = split_image(image, self.config.split_height)
                print(f"✂️  Immagine divisa in {len(images)} chunk")
            else:
                images = [image]

            # 3. Converti ogni chunk in ESC/POS e stampa
            for i, img in enumerate(images):
                print(f"\n📦 Chunk {i+1}/{len(images)}")

                # Converti in comandi ESC/POS
                print("🔄 Conversione in ESC/POS...")
                escpos_data = self.converter.create_print_job(
                    img,
                    init=(i == 0),  # Inizializza solo sul primo chunk
                    cut=(i == len(images) - 1) and self.config.cut_paper,  # Taglia solo sull'ultimo chunk
                    lines_before=self.config.lines_before if i == 0 else 0,
                    lines_after=self.config.lines_after if i == len(images) - 1 else 0
                )

                # Stampa
                print("🖨️  Invio alla stampante...")
                success = self.printer_backend.print(escpos_data)

                if not success:
                    print(f"❌ Errore nella stampa del chunk {i+1}")
                    return False

                # Delay tra chunk se configurato
                if i < len(images) - 1 and self.config.split_delay > 0:
                    import time
                    print(f"⏳ Attesa {self.config.split_delay}s...")
                    time.sleep(self.config.split_delay)

            print(f"\n✅ Stampa completata con successo!")
            return True

        except Exception as e:
            print(f"❌ Errore durante la stampa: {e}")
            import traceback
            traceback.print_exc()
            return False

    def print_text(self, text: str, font_size: int = 12, bold: bool = False, center: bool = False) -> bool:
        """
        Stampa testo semplice.

        Metodo di utilità per stampare testo senza dover creare un template.

        Args:
            text (str): Testo da stampare
            font_size (int): Dimensione del font (default: 12)
            bold (bool): Se True, usa grassetto (default: False)
            center (bool): Se True, centra il testo (default: False)

        Returns:
            bool: True se la stampa è riuscita

        Esempio:
            >>> printer.print_text("Benvenuto!", font_size=24, bold=True, center=True)
            True
        """
        # Crea un template HTML semplice
        template = f"""
        <p style="
            font-size: {font_size}px;
            font-weight: {'bold' if bold else 'normal'};
            text-align: {'center' if center else 'left'};
            margin: 10px 0;
        ">{{ text }}</p>
        """

        return self.print_template(template, {'text': text})

    def feed_paper(self, lines: int = 5) -> bool:
        """
        Avanza la carta di N righe.

        Utile per separare stampe o per estrarre la carta dalla stampante.

        Args:
            lines (int): Numero di righe da avanzare

        Returns:
            bool: True se riuscito
        """
        try:
            print(f"📄 Avanzamento carta di {lines} righe...")
            data = self.converter.feed_lines(lines)
            return self.printer_backend.print(data)
        except Exception as e:
            print(f"❌ Errore: {e}")
            return False

    def cut_paper(self, full_cut: bool = False) -> bool:
        """
        Taglia la carta.

        Args:
            full_cut (bool): Se True, taglio completo. Se False, taglio parziale.

        Returns:
            bool: True se riuscito
        """
        try:
            print(f"✂️  Taglio carta ({'completo' if full_cut else 'parziale'})...")
            data = self.converter.cut_paper(full_cut)
            return self.printer_backend.print(data)
        except Exception as e:
            print(f"❌ Errore: {e}")
            return False

    def test_print(self) -> bool:
        """
        Stampa una pagina di test per verificare il funzionamento.

        Returns:
            bool: True se riuscito
        """
        template = """
        <div style="text-align: center; padding: 20px;">
            <h1 style="margin: 20px 0;">TEST STAMPANTE</h1>
            <p>Thermal Printer Python</p>
            <hr style="margin: 20px 0;">
            <p style="font-size: 10px;">
                Se vedi questo messaggio,<br>
                la stampante funziona correttamente!
            </p>
            <hr style="margin: 20px 0;">
            <p style="font-size: 8px;">
                Larghezza: {{ width }}px<br>
                Tipo: {{ type }}<br>
                Endpoint: {{ endpoint }}
            </p>
        </div>
        """

        return self.print_template(template, {
            'width': self.config.printer_width,
            'type': self.config.printer_type,
            'endpoint': self.config.endpoint
        })

    def close(self):
        """
        Chiude tutte le connessioni e rilascia le risorse.

        Importante: Chiama sempre questo metodo quando hai finito di usare la stampante.
        """
        print("🔌 Chiusura ThermalPrinter...")

        # Chiudi il renderer se è stato inizializzato
        if self.renderer:
            self.renderer.close()
            self.renderer = None

        # Chiudi il backend di stampa
        if self.printer_backend:
            self.printer_backend.close()

        print("✅ ThermalPrinter chiuso")

    def __enter__(self):
        """Supporto per context manager (with statement)"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Chiusura automatica quando si esce dal context manager"""
        self.close()

    def __del__(self):
        """Chiude le risorse quando l'oggetto viene distrutto"""
        try:
            self.close()
        except:
            pass


if __name__ == "__main__":
    # Test della classe ThermalPrinter
    print("🧪 Test ThermalPrinter\n")

    # Crea configurazione di test
    config = PrinterConfig(
        printer_type='network',
        endpoint='192.168.1.100:9100',
        printer_width=384,
        cut_paper=True,
        lines_before=2,
        lines_after=3
    )

    print(config)

    # Nota: Per eseguire questo test, devi avere una stampante configurata!
    print("\n⚠️  Per testare la stampa effettiva, modifica l'endpoint nella configurazione")
    print("   e decomment il codice qui sotto:\n")

    # Decommenta per testare con una stampante reale
    """
    with ThermalPrinter(config) as printer:
        # Test 1: Stampa di test
        print("Test 1: Pagina di test")
        printer.test_print()

        # Test 2: Testo semplice
        print("\nTest 2: Testo semplice")
        printer.print_text("Ciao Mondo!", font_size=18, bold=True, center=True)

        # Test 3: Template personalizzato
        print("\nTest 3: Template personalizzato")
        template = '''
        <div style="padding: 10px;">
            <h2 style="text-align: center;">{{ titolo }}</h2>
            <hr>
            <ul>
            {% for item in items %}
                <li>{{ item.nome }}: €{{ item.prezzo }}</li>
            {% endfor %}
            </ul>
            <hr>
            <p style="text-align: right; font-weight: bold;">
                Totale: €{{ totale }}
            </p>
        </div>
        '''

        printer.print_template(template, {
            'titolo': 'Ricevuta',
            'items': [
                {'nome': 'Caffè', 'prezzo': '1.50'},
                {'nome': 'Cornetto', 'prezzo': '1.20'},
            ],
            'totale': '2.70'
        })
    """
