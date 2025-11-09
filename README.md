# 🖨️ Thermal Printer Python

Una libreria Python completa per stampare contenuti HTML/CSS su stampanti termiche.

**Caratteristiche principali:**
- ✅ Template HTML con Jinja2 (come Nunjucks)
- ✅ Rendering HTML → Immagine con browser headless
- ✅ Conversione automatica in comandi ESC/POS
- ✅ Supporto stampanti Network, USB e Seriali
- ✅ Codice fortemente commentato e facile da capire
- ✅ Esempi pronti all'uso

---

## 📋 Indice

1. [Installazione](#-installazione)
2. [Guida Rapida](#-guida-rapida)
3. [Configurazione Stampante](#-configurazione-stampante)
4. [Esempi d'Uso](#-esempi-duso)
5. [Struttura Progetto](#-struttura-progetto)
6. [Documentazione Componenti](#-documentazione-componenti)
7. [Troubleshooting](#-troubleshooting)

---

## 🚀 Installazione

### 1. Prerequisiti

- Python 3.7 o superiore
- Chrome/Chromium installato sul sistema (per il rendering HTML)

### 2. Installa le dipendenze

```bash
# Entra nella cartella del progetto
cd thermal_printer_python

# Installa tutte le dipendenze
pip install -r requirements.txt
```

### 3. Dipendenze opzionali

**Per stampanti USB (Linux/Mac):**
```bash
# Ubuntu/Debian
sudo apt-get install libusb-1.0-0

# macOS (con Homebrew)
brew install libusb
```

**Per stampanti USB (Windows):**
- Scarica libusb da: https://libusb.info/
- Potrebbe servire Zadig per installare driver WinUSB

---

## ⚡ Guida Rapida

### Esempio Minimo

```python
from thermal_printer import ThermalPrinter, PrinterConfig

# Configura la stampante
config = PrinterConfig(
    printer_type='network',           # 'network', 'serial', o 'usb'
    endpoint='192.168.1.100:9100',   # Indirizzo stampante
    printer_width=384                 # 384px = 58mm, 576px = 80mm
)

# Crea e usa la stampante
with ThermalPrinter(config) as printer:
    # Stampa testo semplice
    printer.print_text("Ciao Mondo!", font_size=20, center=True)

    # Oppure usa un template HTML
    template = "<h1>Ciao {{ nome }}!</h1>"
    printer.print_template(template, {'nome': 'Mario'})
```

---

## ⚙️ Configurazione Stampante

### Configurazione Network (WiFi/Ethernet)

```python
config = PrinterConfig(
    printer_type='network',
    endpoint='192.168.1.100:9100',  # IP:porta (porta standard: 9100)
    printer_width=384
)
```

**Come trovare l'IP della stampante:**
- Stampa pagina di configurazione dalla stampante
- Oppure controlla nel router/DHCP

### Configurazione Seriale (USB-to-Serial)

```python
config = PrinterConfig(
    printer_type='serial',
    endpoint='COM3',  # Windows: COM3, COM4, etc.
                      # Linux: /dev/ttyUSB0, /dev/ttyACM0
                      # Mac: /dev/cu.usbserial
    printer_width=384
)
```

**Come trovare la porta seriale:**
```python
from thermal_printer.printers.serial_printer import SerialPrinter
SerialPrinter.list_available_ports()
```

### Configurazione USB Raw

```python
config = PrinterConfig(
    printer_type='usb',
    endpoint='0x04b8:0x0e15',  # vendorID:productID (formato hex)
    printer_width=384
)
```

**Come trovare Vendor/Product ID:**
```python
from thermal_printer.printers.usb import USBPrinter
USBPrinter.list_usb_devices()
```

### Opzioni Aggiuntive

```python
config = PrinterConfig(
    # ... configurazione base ...

    # Opzioni di stampa
    cut_paper=True,         # Taglia carta automaticamente
    lines_before=2,         # Righe vuote prima del contenuto
    lines_after=3,          # Righe vuote dopo il contenuto

    # Gestione immagini lunghe
    split_printing=True,    # Dividi immagini lunghe
    split_height=1000,      # Altezza massima per chunk (pixel)
    split_delay=0.1,        # Delay tra chunk (secondi)

    # Compatibilità
    use_esc_star=False      # True = usa ESC * (più compatibile ma lento)
                            # False = usa GS v 0 (più veloce)
)
```

### Preset per Stampanti Comuni

```python
from thermal_printer.config import get_preset

# Stampante 58mm
config = get_preset('58mm')  # printer_width=384

# Stampante 80mm
config = get_preset('80mm')  # printer_width=576

# Poi modifica solo quello che serve
config.printer_type = 'network'
config.endpoint = '192.168.1.100:9100'
```

---

## 📚 Esempi d'Uso

### 1. Stampa Testo Semplice

```python
with ThermalPrinter(config) as printer:
    printer.print_text("BENVENUTO", font_size=24, bold=True, center=True)
    printer.print_text("Testo normale", font_size=12)
```

### 2. Stampa con Template HTML

```python
template = """
<div style="padding: 10px;">
    <h1 style="text-align: center;">{{ titolo }}</h1>
    <hr>
    <p>{{ messaggio }}</p>
</div>
"""

dati = {
    'titolo': 'Promemoria',
    'messaggio': 'Non dimenticare di...'
}

with ThermalPrinter(config) as printer:
    printer.print_template(template, dati)
```

### 3. Stampa Ricevuta

Vedi `examples/esempio_ricevuta.py` per un esempio completo con:
- Intestazione negozio
- Lista articoli con prezzi
- Calcolo totali e IVA
- Barcode simulato
- Footer personalizzato

```bash
python examples/esempio_ricevuta.py
```

### 4. Stampa Immagine Esistente

```python
from PIL import Image

with ThermalPrinter(config) as printer:
    # Carica un'immagine
    img = Image.open('logo.png')

    # Stampa
    printer.print_image(img)
```

### 5. Operazioni Utili

```python
with ThermalPrinter(config) as printer:
    # Stampa di test
    printer.test_print()

    # Avanza carta
    printer.feed_paper(5)

    # Taglia carta
    printer.cut_paper()
```

---

## 📁 Struttura Progetto

```
thermal_printer_python/
│
├── src/thermal_printer/          # Codice sorgente
│   ├── __init__.py               # Package principale
│   ├── printer.py                # Classe ThermalPrinter
│   ├── config.py                 # Configurazione
│   │
│   ├── templates/                # Sistema di templating
│   │   ├── template_engine.py   # Motore Jinja2
│   │   └── renderer.py           # Rendering HTML → Immagine
│   │
│   ├── converters/               # Conversione formati
│   │   └── escpos.py             # Immagine → ESC/POS
│   │
│   └── printers/                 # Backend di stampa
│       ├── network.py            # Stampa via rete
│       ├── serial_printer.py    # Stampa via seriale
│       └── usb.py                # Stampa via USB raw
│
├── examples/                     # Esempi d'uso
│   ├── esempio_semplice.py      # Esempio base
│   ├── esempio_ricevuta.py      # Ricevuta completa
│   └── template_ricevuta.html   # Template ricevuta
│
├── docs/                         # Documentazione
│   ├── RENDERING_PIPELINE.md    # Come funziona il rendering
│   └── TROUBLESHOOTING.md        # Risoluzione problemi
│
├── requirements.txt              # Dipendenze Python
├── README.md                     # Questo file
└── TODO.md                       # Lista implementazioni
```

---

## 🔧 Documentazione Componenti

### ThermalPrinter (Classe Principale)

La classe principale che coordina tutti i componenti.

```python
from thermal_printer import ThermalPrinter, PrinterConfig

config = PrinterConfig(...)
printer = ThermalPrinter(config)

# Metodi principali:
printer.print_template(template_string, data)  # Stampa template
printer.print_text(text, font_size, ...)       # Stampa testo
printer.print_image(image)                     # Stampa immagine PIL
printer.test_print()                           # Stampa di test
printer.feed_paper(lines)                      # Avanza carta
printer.cut_paper()                            # Taglia carta
printer.close()                                # Chiudi stampante
```

### TemplateEngine (Jinja2)

Renderizza template HTML con dati dinamici.

```python
from thermal_printer.templates.template_engine import TemplateEngine

engine = TemplateEngine()

# Renderizza da stringa
html = engine.render_string(
    "<h1>{{ title }}</h1>",
    {'title': 'Ciao'}
)

# Aggiungi filtri custom
engine.env.filters['maiuscolo'] = str.upper

# Usa nei template: {{ testo|maiuscolo }}
```

**Sintassi Jinja2:**
- `{{ variabile }}` - Stampa valore
- `{% if condizione %}...{% endif %}` - Condizionale
- `{% for item in lista %}...{% endfor %}` - Ciclo
- `{{ valore|filtro }}` - Applica filtro

### HTMLRenderer

Converte HTML in immagini PNG.

```python
from thermal_printer.templates.renderer import HTMLRenderer

renderer = HTMLRenderer(width=384, method='html2image')

# Renderizza HTML
html = "<h1>Test</h1>"
image = renderer.render_html(html)

# Salva immagine
image.save('output.png')

renderer.close()
```

### ESCPOSConverter

Converte immagini in comandi ESC/POS.

```python
from thermal_printer.converters.escpos import ESCPOSConverter
from PIL import Image

converter = ESCPOSConverter(use_esc_star=False)

# Carica immagine
img = Image.open('test.png')

# Converti in comandi ESC/POS
commands = converter.create_print_job(
    img,
    init=True,
    cut=True,
    lines_before=2,
    lines_after=3
)

# Ora 'commands' è un bytes con i comandi da inviare alla stampante
```

### Backend di Stampa

Tre backend per comunicare con la stampante:

**Network:**
```python
from thermal_printer.printers.network import NetworkPrinter

printer = NetworkPrinter('192.168.1.100', 9100)
printer.connect()
printer.print(escpos_commands)
printer.close()
```

**Serial:**
```python
from thermal_printer.printers.serial_printer import SerialPrinter

printer = SerialPrinter('COM3', baudrate=9600)
printer.connect()
printer.print(escpos_commands)
printer.close()
```

**USB:**
```python
from thermal_printer.printers.usb import USBPrinter

printer = USBPrinter(0x04b8, 0x0e15)  # vendor_id, product_id
printer.connect()
printer.print(escpos_commands)
printer.close()
```

---

## 🆘 Troubleshooting

### Problema: Libreria non trovata

```
ModuleNotFoundError: No module named 'thermal_printer'
```

**Soluzione:**
```bash
# Assicurati di essere nella cartella del progetto
cd thermal_printer_python

# Aggiungi src/ al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Oppure esegui da Python aggiungendo il path:
import sys
sys.path.insert(0, 'src')
```

### Problema: html2image non trova Chrome

```
Error: Chrome/Chromium not found
```

**Soluzione:**
- **Windows**: Installa Chrome da https://www.google.com/chrome/
- **Linux**: `sudo apt-get install chromium-browser`
- **macOS**: `brew install chromium`

### Problema: Stampante network non si connette

```
Error: Connection timeout
```

**Verifica:**
```python
from thermal_printer.printers.network import NetworkPrinter

# Testa la connessione
printer = NetworkPrinter('192.168.1.100', 9100, timeout=5.0)
if printer.connect():
    print("Connesso!")
else:
    print("Connessione fallita")
```

**Cause comuni:**
- Stampante spenta
- IP errato (verifica sulla stampante)
- Firewall che blocca la porta 9100
- Stampante non sulla stessa rete

### Problema: Porta seriale non trovata

```
Error: Could not open port COM3
```

**Soluzione:**
```python
# Lista tutte le porte disponibili
from thermal_printer.printers.serial_printer import SerialPrinter
SerialPrinter.list_available_ports()
```

**Su Linux:** Potrebbe servire aggiungere l'utente al gruppo `dialout`:
```bash
sudo usermod -a -G dialout $USER
# Poi logout/login
```

### Problema: USB device not found

```
Error: Device not found
```

**Soluzione:**
```python
# Lista tutti i dispositivi USB
from thermal_printer.printers.usb import USBPrinter
USBPrinter.list_usb_devices()
```

**Su Linux:** Potrebbe servire permessi sudo o una regola udev:
```bash
# Crea file /etc/udev/rules.d/99-thermal-printer.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="04b8", ATTR{idProduct}=="0e15", MODE="0666"

# Ricarica regole
sudo udevadm control --reload-rules
```

### Problema: Stampa esce bianca

**Cause:**
- Carta termica inserita al contrario (lato termico va verso la testina)
- Immagine troppo chiara
- Threshold di conversione bianco/nero troppo alto

**Soluzione:**
Modifica il threshold in `escpos.py`:
```python
# In ESCPOSConverter._convert_to_bw()
# Abbassa il threshold (default 128)
image_bw = image.point(lambda x: 0 if x < 100 else 255, '1')
```

---

## 📖 Risorse Aggiuntive

### Documentazione

- `docs/RENDERING_PIPELINE.md` - Spiegazione dettagliata di come funziona il rendering
- `docs/TROUBLESHOOTING.md` - Guida alla risoluzione problemi
- `TODO.md` - Lista delle implementazioni con spiegazioni

### Esempio di Template HTML

Vedi `examples/template_ricevuta.html` per un template completo di ricevuta con:
- Stili CSS responsive
- Layout professionale
- Tabelle e separatori
- Footer e header

### ESC/POS Reference

Comandi ESC/POS supportati:
- `ESC @` - Inizializza stampante
- `GS v 0` - Stampa immagine raster (veloce)
- `ESC *` - Stampa immagine 24-dot (compatibile)
- `GS V` - Taglia carta
- `LF` - Avanza carta

Documentazione completa: [Epson ESC/POS Programming Manual](https://reference.epson-biz.com/modules/ref_escpos/)

---

## 🤝 Contribuire

Questo è un progetto educativo. Sentiti libero di:
- Aggiungere nuove funzionalità
- Migliorare i commenti
- Creare nuovi esempi
- Segnalare bug

---

## 📄 Licenza

Questo progetto è fornito "as-is" a scopo educativo.

---

## ❓ Domande Frequenti

**Q: Posso usare questa libreria in produzione?**
A: Sì, ma testa bene con la tua stampante specifica. Ogni modello può avere piccole differenze.

**Q: Funziona con stampanti Bluetooth?**
A: Non direttamente. Dovresti creare un backend Bluetooth simile a quelli esistenti.

**Q: Posso stampare immagini a colori?**
A: No, le stampanti termiche sono solo bianco/nero. Le immagini vengono convertite automaticamente.

**Q: Quanto è veloce la stampa?**
A: Dipende dalla stampante e dal metodo di connessione. Network è generalmente il più veloce.

**Q: Posso cambiare il font?**
A: Sì, usa CSS nel template HTML: `font-family: 'Arial', sans-serif`

---

## 🎓 Per Imparare

Se non sei un programmatore, ecco cosa devi sapere:

1. **Python**: Linguaggio di programmazione facile da imparare
2. **HTML/CSS**: Per creare i template (come le pagine web)
3. **Jinja2**: Template engine (simile a Nunjucks)
4. **ESC/POS**: Linguaggio comandi delle stampanti termiche

**Risorse consigliate:**
- Python: https://www.python.org/about/gettingstarted/
- HTML/CSS: https://www.w3schools.com/
- Jinja2: https://jinja.palletsprojects.com/

---

**Buona stampa! 🖨️**
