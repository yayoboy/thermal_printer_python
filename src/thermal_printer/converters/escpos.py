"""
Convertitore Immagine -> ESC/POS
=================================

Questo modulo converte immagini PIL in comandi ESC/POS per stampanti termiche.

ESC/POS è il linguaggio di comando standard per stampanti termiche.
I comandi principali sono:
- ESC @ : Inizializza la stampante
- GS v 0 : Stampa immagine in modalità raster
- ESC * : Stampa immagine in modalità 24-dot (più compatibile)
- GS V : Taglia la carta
"""

from PIL import Image
from typing import List
import io


class ESCPOSConverter:
    """
    Converte immagini in comandi ESC/POS per stampanti termiche.

    Questa classe prende un'immagine PIL e la converte in una sequenza
    di byte che rappresentano comandi ESC/POS comprensibili dalla stampante.

    Esempio:
        >>> converter = ESCPOSConverter()
        >>> image = Image.open('logo.png')
        >>> commands = converter.image_to_escpos(image)
        >>> # Ora 'commands' contiene i byte da inviare alla stampante
    """

    # Comandi ESC/POS come costanti
    ESC = b'\x1b'   # ESC character (27 decimale, 0x1B esadecimale)
    GS = b'\x1d'    # GS character (29 decimale, 0x1D esadecimale)
    LF = b'\n'      # Line feed (newline)

    def __init__(self, use_esc_star: bool = False):
        """
        Inizializza il convertitore.

        Args:
            use_esc_star (bool): Se True, usa ESC * invece di GS v 0.
                ESC * è più compatibile con stampanti vecchie, ma più lento.
        """
        self.use_esc_star = use_esc_star

    def init_printer(self) -> bytes:
        """
        Genera il comando per inizializzare la stampante.

        Il comando ESC @ resetta la stampante allo stato iniziale,
        cancellando buffer e impostazioni precedenti.

        Returns:
            bytes: Comando ESC @ (ESC + @)
        """
        return self.ESC + b'@'

    def cut_paper(self, full_cut: bool = False) -> bytes:
        """
        Genera il comando per tagliare la carta.

        Args:
            full_cut (bool): Se True, taglio completo. Se False, taglio parziale.
                Il taglio parziale lascia una piccola parte attaccata per facilitare
                lo strappo manuale.

        Returns:
            bytes: Comando GS V per il taglio
        """
        # GS V m (m = 0 per taglio completo, m = 1 per taglio parziale)
        cut_type = b'\x00' if full_cut else b'\x01'
        return self.GS + b'V' + cut_type

    def feed_lines(self, lines: int) -> bytes:
        """
        Genera comandi per avanzare la carta di N righe.

        Args:
            lines (int): Numero di righe da avanzare

        Returns:
            bytes: Sequenza di caratteri newline (\n)
        """
        return self.LF * lines

    def image_to_escpos(self, image: Image.Image) -> bytes:
        """
        Converte un'immagine PIL in comandi ESC/POS.

        Questo è il metodo principale che fa la conversione.

        Args:
            image (PIL.Image.Image): Immagine da convertire

        Returns:
            bytes: Sequenza di comandi ESC/POS per stampare l'immagine

        Processo:
            1. Converte l'immagine in bianco/nero
            2. Per ogni riga di pixel, crea un comando ESC/POS
            3. Ogni byte rappresenta 8 pixel (1 bit per pixel)
        """
        if self.use_esc_star:
            return self._image_to_esc_star(image)
        else:
            return self._image_to_raster(image)

    def _image_to_raster(self, image: Image.Image) -> bytes:
        """
        Converte immagine usando modalità GS v 0 (raster).

        Questa è la modalità moderna e più veloce.

        Formato comando: GS v 0 m xL xH yL yH [dati immagine]
        - m = 0 (modalità normale)
        - xL xH = larghezza in byte (little-endian)
        - yL yH = altezza in pixel (little-endian)
        - dati = bitmap (1 bit per pixel, 1 = nero, 0 = bianco)

        Args:
            image (PIL.Image.Image): Immagine da convertire

        Returns:
            bytes: Comandi ESC/POS in modalità raster
        """
        # Converti in modalità 1-bit (bianco/nero)
        image_bw = self._convert_to_bw(image)

        # Ottieni dimensioni
        width, height = image_bw.size

        # Calcola larghezza in byte (ogni byte = 8 pixel)
        width_bytes = (width + 7) // 8  # Arrotonda per eccesso

        # Buffer per i comandi
        buffer = io.BytesIO()

        # Per ogni riga di pixel
        for y in range(height):
            # Comando: GS v 0 m xL xH yL yH
            buffer.write(self.GS + b'v0' + b'\x00')  # GS v 0 m (m=0)

            # Larghezza in byte (little-endian: byte basso, byte alto)
            buffer.write(bytes([width_bytes & 0xFF, (width_bytes >> 8) & 0xFF]))

            # Altezza (stampiamo 1 riga alla volta)
            buffer.write(b'\x01\x00')  # 1 riga (little-endian)

            # Converti la riga in bitmap
            line_data = self._convert_line_to_bitmap(image_bw, y, width_bytes)
            buffer.write(line_data)

        return buffer.getvalue()

    def _image_to_esc_star(self, image: Image.Image) -> bytes:
        """
        Converte immagine usando modalità ESC * (24-dot).

        Questa modalità è più compatibile con stampanti vecchie,
        ma più lenta perché elabora 24 righe alla volta.

        Formato comando: ESC * m nL nH [dati]
        - m = 24 (24-dot double density)
        - nL nH = larghezza in pixel (little-endian)
        - dati = bitmap verticale (3 byte per colonna, 24 pixel verticali)

        Args:
            image (PIL.Image.Image): Immagine da convertire

        Returns:
            bytes: Comandi ESC/POS in modalità ESC *
        """
        # Converti in bianco/nero
        image_bw = self._convert_to_bw(image)
        width, height = image_bw.size

        # Buffer per i comandi
        buffer = io.BytesIO()

        # Elabora 24 righe alla volta
        for y in range(0, height, 24):
            # Comando: ESC * m nL nH
            buffer.write(self.ESC + b'*' + bytes([24]))  # ESC * 24

            # Larghezza in pixel (little-endian)
            buffer.write(bytes([width & 0xFF, (width >> 8) & 0xFF]))

            # Per ogni colonna di pixel
            for x in range(width):
                # 3 byte per 24 pixel verticali
                col_bytes = [0, 0, 0]

                # Leggi 24 pixel verticali
                for bit in range(24):
                    if y + bit < height:
                        # Ottieni il pixel
                        pixel = image_bw.getpixel((x, y + bit))

                        # Se il pixel è nero (0), imposta il bit
                        if pixel == 0:
                            byte_pos = bit // 8  # Quale dei 3 byte
                            bit_pos = 7 - (bit % 8)  # Posizione del bit nel byte
                            col_bytes[byte_pos] |= (1 << bit_pos)

                # Scrivi i 3 byte
                buffer.write(bytes(col_bytes))

            # Newline dopo ogni banda di 24 righe
            buffer.write(self.LF)

        return buffer.getvalue()

    def _convert_to_bw(self, image: Image.Image, threshold: int = 128) -> Image.Image:
        """
        Converte un'immagine a colori in bianco/nero puro.

        Le stampanti termiche stampano solo in bianco/nero,
        quindi dobbiamo convertire l'immagine.

        Args:
            image (PIL.Image.Image): Immagine da convertire
            threshold (int): Soglia per decidere bianco/nero (0-255).
                Pixel con luminosità < threshold diventano neri.

        Returns:
            PIL.Image.Image: Immagine in modalità '1' (1 bit per pixel)

        Processo:
            1. Converti in grayscale (L = luminosità)
            2. Applica threshold: < 128 = nero, >= 128 = bianco
            3. Converti in modalità '1' (1 bit)
        """
        # Converti in grayscale se necessario
        if image.mode != 'L':
            image = image.convert('L')

        # Converti in bianco/nero con threshold
        image_bw = image.point(lambda x: 0 if x < threshold else 255, '1')

        return image_bw

    def _convert_line_to_bitmap(self, image_bw: Image.Image, y: int, width_bytes: int) -> bytes:
        """
        Converte una singola riga di pixel in bitmap.

        Ogni byte contiene 8 pixel (1 bit per pixel).
        Bit = 1 significa nero, bit = 0 significa bianco.

        Args:
            image_bw (PIL.Image.Image): Immagine bianco/nero
            y (int): Numero della riga da convertire
            width_bytes (int): Quanti byte servono per la riga

        Returns:
            bytes: Bitmap della riga

        Esempio:
            Se la riga ha 10 pixel: NBNNNBBBNN (N=nero, B=bianco)
            Servono 2 byte (8 + 2 pixel):
            Byte 1: 10111000 (primi 8 pixel)
            Byte 2: 11000000 (ultimi 2 pixel + 6 zero di padding)
        """
        width = image_bw.size[0]
        line_data = []

        # Per ogni byte nella riga
        for byte_x in range(width_bytes):
            byte_val = 0

            # Leggi 8 pixel
            for bit in range(8):
                x = byte_x * 8 + bit

                # Se siamo ancora dentro l'immagine
                if x < width:
                    # Ottieni il pixel (0 = nero, 255 = bianco in modalità '1')
                    pixel = image_bw.getpixel((x, y))

                    # Se è nero, imposta il bit
                    # Nota: in modalità '1', 0 = nero, quindi invertiamo
                    if pixel == 0:
                        bit_pos = 7 - bit  # MSB first (bit più significativo per primo)
                        byte_val |= (1 << bit_pos)

            line_data.append(byte_val)

        return bytes(line_data)

    def create_print_job(
        self,
        image: Image.Image,
        init: bool = True,
        cut: bool = True,
        lines_before: int = 0,
        lines_after: int = 0
    ) -> bytes:
        """
        Crea un job di stampa completo per un'immagine.

        Questo metodo combina tutti i comandi necessari:
        inizializzazione, righe vuote, immagine, taglio carta.

        Args:
            image (PIL.Image.Image): Immagine da stampare
            init (bool): Se True, inizializza la stampante
            cut (bool): Se True, taglia la carta alla fine
            lines_before (int): Righe vuote prima dell'immagine
            lines_after (int): Righe vuote dopo l'immagine

        Returns:
            bytes: Sequenza completa di comandi ESC/POS

        Esempio:
            >>> converter = ESCPOSConverter()
            >>> img = Image.open('receipt.png')
            >>> commands = converter.create_print_job(img, init=True, cut=True, lines_before=2, lines_after=3)
            >>> # Ora invia 'commands' alla stampante
        """
        buffer = io.BytesIO()

        # 1. Inizializza stampante (opzionale)
        if init:
            buffer.write(self.init_printer())

        # 2. Righe vuote prima
        if lines_before > 0:
            buffer.write(self.feed_lines(lines_before))

        # 3. Immagine
        buffer.write(self.image_to_escpos(image))

        # 4. Righe vuote dopo
        if lines_after > 0:
            buffer.write(self.feed_lines(lines_after))

        # 5. Taglia carta (opzionale)
        if cut:
            buffer.write(self.cut_paper(full_cut=False))

        return buffer.getvalue()


def split_image(image: Image.Image, max_height: int) -> List[Image.Image]:
    """
    Divide un'immagine in più parti se è troppo alta.

    Questo è utile per immagini molto lunghe che potrebbero causare
    problemi di memoria o timeout sulla stampante.

    Args:
        image (PIL.Image.Image): Immagine da dividere
        max_height (int): Altezza massima di ogni parte in pixel

    Returns:
        List[PIL.Image.Image]: Lista di immagini più piccole

    Esempio:
        >>> img = Image.open('long_receipt.png')  # 2000px di altezza
        >>> chunks = split_image(img, 1000)  # Dividi in chunk da 1000px
        >>> len(chunks)
        2
    """
    width, height = image.size

    # Se l'immagine è già abbastanza piccola, restituiscila così
    if height <= max_height:
        return [image]

    # Calcola quante parti servono
    num_chunks = (height + max_height - 1) // max_height

    # Dividi l'immagine
    chunks = []
    for i in range(num_chunks):
        # Calcola coordinate di taglio
        y1 = i * max_height
        y2 = min(y1 + max_height, height)

        # Ritaglia la parte
        chunk = image.crop((0, y1, width, y2))
        chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    # Test del convertitore
    print("🧪 Test del ESC/POS Converter\n")

    # Crea un'immagine di test semplice
    test_image = Image.new('RGB', (384, 100), color='white')

    # Disegna qualcosa sull'immagine
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(test_image)

    # Disegna un rettangolo
    draw.rectangle([10, 10, 374, 90], outline='black', width=2)

    # Scrivi del testo
    draw.text((50, 40), "TEST STAMPANTE", fill='black')

    # Test conversione
    converter = ESCPOSConverter(use_esc_star=False)

    # Crea job di stampa completo
    commands = converter.create_print_job(
        test_image,
        init=True,
        cut=True,
        lines_before=2,
        lines_after=3
    )

    print(f"✅ Comandi ESC/POS generati: {len(commands)} bytes")
    print(f"   Primi 20 bytes: {commands[:20].hex()}")
    print(f"\n   Interpretazione:")
    print(f"   - ESC @ (init): {commands[0:2].hex()}")
    print(f"   - Newline x2: {commands[2:4].hex()}")
    print(f"   - GS v 0 (immagine raster): {commands[4:8].hex()}")
    print(f"   - ... dati immagine ...")
    print(f"   - Ultimi 10 bytes: {commands[-10:].hex()}")

    # Test split
    print(f"\n🧪 Test split immagine:")
    big_image = Image.new('RGB', (384, 2500), color='white')
    chunks = split_image(big_image, 1000)
    print(f"   Immagine {big_image.size[0]}x{big_image.size[1]}px")
    print(f"   Divisa in {len(chunks)} chunk")
    for i, chunk in enumerate(chunks):
        print(f"   - Chunk {i+1}: {chunk.size[0]}x{chunk.size[1]}px")
