"""
HTML to Image Renderer
======================

Questo modulo converte HTML in immagini PNG usando un browser headless.

Supporta due metodi:
1. html2image (più semplice, non richiede driver)
2. Selenium + Chrome (più potente, rendering migliore)
"""

from PIL import Image
from typing import Optional, Tuple
import io
import tempfile
import os


class HTMLRenderer:
    """
    Classe per renderizzare HTML in immagini.

    Questa classe prende HTML (con CSS) e lo converte in un'immagine PNG
    che può essere stampata sulla stampante termica.

    Esempio:
        >>> renderer = HTMLRenderer(width=384)
        >>> image = renderer.render_html("<h1>Ciao!</h1>")
        >>> image.save("output.png")
    """

    def __init__(self, width: int = 384, method: str = 'html2image'):
        """
        Inizializza il renderer.

        Args:
            width (int): Larghezza dell'immagine in pixel (default: 384px per stampanti 58mm)
            method (str): Metodo di rendering ('html2image' o 'selenium')
                - 'html2image': Più semplice, non richiede driver esterni
                - 'selenium': Rendering migliore, richiede Chrome/Chromium installato
        """
        self.width = width
        self.method = method

        # Inizializza il metodo di rendering scelto
        if method == 'selenium':
            self._init_selenium()
        elif method == 'html2image':
            self._init_html2image()
        else:
            raise ValueError(f"Metodo '{method}' non supportato. Usa 'html2image' o 'selenium'.")

    def _init_html2image(self):
        """
        Inizializza il renderer html2image.

        html2image usa Chrome/Chromium headless per renderizzare HTML.
        Non richiede driver esterni come Selenium.
        """
        try:
            from html2image import Html2Image
            self.hti = Html2Image()
            # Imposta dimensioni di output
            self.hti.size = (self.width, 10000)  # Altezza grande per auto-scroll
        except ImportError:
            raise ImportError(
                "html2image non installato. Installa con: pip install html2image\n"
                "Nota: Richiede Chrome o Chromium installato sul sistema."
            )

    def _init_selenium(self):
        """
        Inizializza il renderer Selenium.

        Selenium usa Chrome/Chromium via WebDriver per renderizzare HTML.
        Offre più controllo ma richiede ChromeDriver.
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service

            # Configurazione Chrome headless (senza finestra)
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Nessuna finestra grafica
            chrome_options.add_argument('--no-sandbox')  # Necessario in alcuni sistemi
            chrome_options.add_argument('--disable-dev-shm-usage')  # Migliora stabilità
            chrome_options.add_argument('--disable-gpu')  # Disabilita GPU (headless)
            chrome_options.add_argument(f'--window-size={self.width},10000')  # Dimensioni finestra

            # Crea il driver Chrome
            # Nota: Richiede ChromeDriver installato e nel PATH
            self.driver = webdriver.Chrome(options=chrome_options)

        except ImportError:
            raise ImportError(
                "Selenium non installato. Installa con: pip install selenium\n"
                "Nota: Richiede anche ChromeDriver installato: https://chromedriver.chromium.org/"
            )
        except Exception as e:
            raise RuntimeError(
                f"Errore nell'inizializzazione Selenium: {e}\n"
                "Assicurati che Chrome/Chromium e ChromeDriver siano installati."
            )

    def render_html(self, html: str, output_path: Optional[str] = None) -> Image.Image:
        """
        Renderizza HTML in un'immagine PNG.

        Questo è il metodo principale che converte HTML in immagine.

        Args:
            html (str): Codice HTML completo da renderizzare
            output_path (str, opzionale): Path dove salvare l'immagine.
                Se None, non salva su file.

        Returns:
            PIL.Image.Image: Immagine renderizzata

        Esempio:
            >>> renderer = HTMLRenderer(384)
            >>> img = renderer.render_html("<h1>Test</h1>")
            >>> print(f"Dimensioni immagine: {img.size}")
            Dimensioni immagine: (384, 150)
        """
        # Usa il metodo appropriato
        if self.method == 'html2image':
            return self._render_html2image(html, output_path)
        elif self.method == 'selenium':
            return self._render_selenium(html, output_path)

    def _render_html2image(self, html: str, output_path: Optional[str]) -> Image.Image:
        """
        Renderizza HTML usando html2image.

        Args:
            html (str): HTML da renderizzare
            output_path (str, opzionale): Dove salvare l'immagine

        Returns:
            PIL.Image.Image: Immagine renderizzata
        """
        # Crea un file temporaneo per salvare l'immagine
        if output_path is None:
            # Se non specificato, usa file temporaneo
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            output_path = temp_file.name
            temp_file.close()
            is_temp = True
        else:
            is_temp = False

        # Ottieni il nome del file senza path
        filename = os.path.basename(output_path)
        output_dir = os.path.dirname(output_path) or '.'

        # Renderizza HTML -> PNG
        self.hti.screenshot(
            html_str=html,
            save_as=filename,
            size=(self.width, 10000)  # Larghezza fissa, altezza auto
        )

        # Carica l'immagine con PIL
        image = Image.open(filename)

        # Converti in RGB se necessario (le stampanti termiche usano RGB/L)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Ritaglia l'immagine all'altezza effettiva del contenuto
        image = self._crop_to_content(image)

        # Se era temporaneo, elimina il file
        if is_temp:
            try:
                os.unlink(output_path)
            except:
                pass

        return image

    def _render_selenium(self, html: str, output_path: Optional[str]) -> Image.Image:
        """
        Renderizza HTML usando Selenium.

        Args:
            html (str): HTML da renderizzare
            output_path (str, opzionale): Dove salvare l'immagine

        Returns:
            PIL.Image.Image: Immagine renderizzata
        """
        # Crea un file HTML temporaneo
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            html_path = f.name

        try:
            # Carica l'HTML nel browser
            self.driver.get(f'file://{html_path}')

            # Aspetta che la pagina sia caricata
            import time
            time.sleep(0.5)  # Piccolo delay per assicurarsi che tutto sia renderizzato

            # Ottieni l'altezza totale della pagina
            total_height = self.driver.execute_script("return document.body.scrollHeight")

            # Imposta le dimensioni della finestra all'altezza totale
            self.driver.set_window_size(self.width, total_height)

            # Prendi uno screenshot
            screenshot_bytes = self.driver.get_screenshot_as_png()

            # Converti bytes in PIL Image
            image = Image.open(io.BytesIO(screenshot_bytes))

            # Converti in RGB se necessario
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Salva se richiesto
            if output_path:
                image.save(output_path, 'PNG')

            return image

        finally:
            # Pulisci il file HTML temporaneo
            try:
                os.unlink(html_path)
            except:
                pass

    def _crop_to_content(self, image: Image.Image) -> Image.Image:
        """
        Ritaglia l'immagine all'altezza del contenuto effettivo.

        Rimuove lo spazio bianco in eccesso in fondo all'immagine.

        Args:
            image (PIL.Image.Image): Immagine da ritagliare

        Returns:
            PIL.Image.Image: Immagine ritagliata
        """
        # Converti in RGB se non lo è già
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Ottieni i pixel dell'immagine
        pixels = image.load()
        width, height = image.size

        # Trova l'ultima riga non bianca (partendo dal basso)
        last_content_row = height - 1
        for y in range(height - 1, -1, -1):
            # Controlla se la riga ha contenuto (non è tutta bianca)
            is_blank = True
            for x in range(width):
                r, g, b = pixels[x, y]
                # Se il pixel non è bianco (255, 255, 255)
                if r < 250 or g < 250 or b < 250:
                    is_blank = False
                    break

            if not is_blank:
                last_content_row = y
                break

        # Ritaglia l'immagine (aggiungi un po' di margine)
        margin = 10
        crop_height = min(last_content_row + margin, height)

        # Se l'immagine è già alla dimensione giusta, restituiscila così com'è
        if crop_height >= height - 10:
            return image

        # Ritaglia
        return image.crop((0, 0, width, crop_height))

    def close(self):
        """
        Chiude il renderer e rilascia le risorse.

        Importante: Chiama sempre questo metodo quando hai finito,
        specialmente se usi Selenium (per chiudere il browser).
        """
        if self.method == 'selenium' and hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except:
                pass

    def __enter__(self):
        """Supporto per context manager (with statement)"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Chiusura automatica quando si esce dal context manager"""
        self.close()


if __name__ == "__main__":
    # Test del renderer
    print("🧪 Test del HTML Renderer\n")

    # HTML di test
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
                width: 384px;
                background: white;
            }
            h1 {
                color: black;
                text-align: center;
            }
            .box {
                border: 2px solid black;
                padding: 10px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <h1>Test Stampante</h1>
        <div class="box">
            <p>Questa è una prova di rendering HTML.</p>
            <p>Larghezza: 384px (stampante 58mm)</p>
        </div>
    </body>
    </html>
    """

    try:
        # Prova con html2image
        print("Tentativo rendering con html2image...")
        with HTMLRenderer(width=384, method='html2image') as renderer:
            img = renderer.render_html(test_html, 'test_output.png')
            print(f"✅ Immagine creata: {img.size[0]}x{img.size[1]}px")
            print(f"   Salvata in: test_output.png")

    except Exception as e:
        print(f"❌ Errore html2image: {e}")
        print("\nProva a installare: pip install html2image")
        print("E assicurati che Chrome/Chromium sia installato.")
