# 🚀 Guida All'Installazione

Guida passo-passo per installare e configurare **Thermal Printer Python**.

---

## 📋 Requisiti

### Sistema Operativo

- ✅ Windows 10/11
- ✅ macOS 10.14 o superiore
- ✅ Linux (Ubuntu 20.04+, Debian, Fedora, etc.)

### Software

- **Python 3.7 o superiore**
  - Verifica versione: `python --version`
  - Download: https://www.python.org/downloads/

- **Chrome/Chromium** (per il rendering HTML)
  - Windows/Mac: https://www.google.com/chrome/
  - Linux: `sudo apt-get install chromium-browser`

---

## 🔧 Installazione

### Passo 1: Scarica il Progetto

```bash
# Se hai git installato
git clone <repository-url>
cd thermal_printer_python

# Oppure scarica e estrai lo ZIP
```

### Passo 2: Crea Ambiente Virtuale (Consigliato)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Installa Dipendenze

```bash
pip install -r requirements.txt
```

Questo installerà:
- jinja2 (templating)
- Pillow (manipolazione immagini)
- html2image (rendering HTML)
- pyserial (stampanti seriali)
- pyusb (stampanti USB)

---

## 🖨️ Configurazione Stampante

### Opzione A: Stampante di Rete (WiFi/Ethernet)

**1. Trova l'IP della stampante:**

- Stampa pagina di configurazione dalla stampante
- Oppure controlla nel router (solitamente 192.168.1.x)

**2. Testa la connessione:**

```python
from thermal_printer.printers.network import NetworkPrinter

# Sostituisci con l'IP della tua stampante
printer = NetworkPrinter('192.168.1.100', 9100)

if printer.connect():
    print("✅ Connessione riuscita!")
else:
    print("❌ Connessione fallita")
```

**3. Configurazione:**

```python
from thermal_printer import PrinterConfig

config = PrinterConfig(
    printer_type='network',
    endpoint='192.168.1.100:9100',  # Tuo IP:porta
    printer_width=384                # 384px = 58mm
)
```

### Opzione B: Stampante Seriale (USB-to-Serial)

**1. Trova la porta seriale:**

**Windows:**
- Gestione Dispositivi → Porte COM
- Solitamente COM3, COM4, etc.

**Linux:**
```bash
ls /dev/ttyUSB*
# Output: /dev/ttyUSB0
```

**Mac:**
```bash
ls /dev/cu.usbserial*
# Output: /dev/cu.usbserial-A1B2C3D4
```

**2. Lista porte con Python:**

```python
from thermal_printer.printers.serial_printer import SerialPrinter

SerialPrinter.list_available_ports()
```

**3. Configurazione:**

```python
config = PrinterConfig(
    printer_type='serial',
    endpoint='COM3',        # Windows
    # endpoint='/dev/ttyUSB0',  # Linux
    # endpoint='/dev/cu.usbserial-xxx',  # Mac
    printer_width=384
)
```

**4. Permessi (Solo Linux):**

Se ricevi errore di permessi:
```bash
sudo usermod -a -G dialout $USER
# Poi logout e login
```

### Opzione C: Stampante USB Raw

**1. Trova Vendor ID e Product ID:**

**Windows:**
- Gestione Dispositivi → Proprietà USB → Dettagli
- Cerca VID e PID

**Linux:**
```bash
lsusb
# Output esempio:
# Bus 001 Device 003: ID 04b8:0e15 Epson Corp.
#                        ^^^^ ^^^^
#                        VID  PID
```

**2. Lista con Python:**

```python
from thermal_printer.printers.usb import USBPrinter

USBPrinter.list_usb_devices()
```

**3. Configurazione:**

```python
config = PrinterConfig(
    printer_type='usb',
    endpoint='0x04b8:0x0e15',  # VID:PID in esadecimale
    printer_width=384
)
```

**4. Driver USB (Windows):**

Su Windows potrebbe servire installare driver WinUSB con **Zadig**:
- Download: https://zadig.akeo.ie/
- Seleziona la stampante
- Installa driver WinUSB

**5. Permessi (Linux):**

Crea file `/etc/udev/rules.d/99-thermal-printer.rules`:
```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="04b8", ATTR{idProduct}=="0e15", MODE="0666"
```

Ricarica regole:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

## ✅ Verifica Installazione

### Test 1: Importa la Libreria

```python
import sys
sys.path.insert(0, 'src')  # Se non installato con pip

from thermal_printer import ThermalPrinter, PrinterConfig

print("✅ Libreria importata con successo!")
```

### Test 2: Stampa di Test

```python
from thermal_printer import ThermalPrinter, PrinterConfig

# Usa la tua configurazione
config = PrinterConfig(
    printer_type='network',  # o 'serial', 'usb'
    endpoint='192.168.1.100:9100',
    printer_width=384
)

# Stampa di test
with ThermalPrinter(config) as printer:
    printer.test_print()
```

Se vedi una stampa con "TEST STAMPANTE", tutto funziona! 🎉

---

## 🆘 Problemi Comuni

### Problema: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'thermal_printer'
```

**Soluzione:**
```python
import sys
sys.path.insert(0, 'src')  # Aggiungi src/ al path
```

Oppure installa come package:
```bash
pip install -e .
```

### Problema: Chrome non trovato

```
Error: Chrome/Chromium not found
```

**Soluzione:**
- Windows: Installa Chrome da https://www.google.com/chrome/
- Linux: `sudo apt-get install chromium-browser`
- Mac: `brew install chromium`

### Problema: Stampante non si connette

**Verifica:**
1. Stampante accesa? ✓
2. Cavo collegato? ✓
3. IP/porta corretti? ✓
4. Firewall blocca? ✓

**Test connessione network:**
```bash
ping 192.168.1.100
telnet 192.168.1.100 9100
```

**Test porta seriale:**
```python
from thermal_printer.printers.serial_printer import SerialPrinter
SerialPrinter.list_available_ports()
```

### Problema: Immagine esce bianca

**Cause:**
- Carta termica girata (lato termico deve toccare testina)
- Carta esaurita o di bassa qualità
- Threshold conversione bianco/nero troppo alto

**Soluzione:**
Abbassa threshold in `escpos.py`:
```python
# Linea ~200 circa
# Cambia da 128 a 100
image_bw = image.point(lambda x: 0 if x < 100 else 255, '1')
```

---

## 📝 Prossimi Passi

1. **Esplora gli esempi:**
   ```bash
   cd examples
   python esempio_semplice.py
   python esempio_ricevuta.py
   ```

2. **Leggi la documentazione:**
   - `README.md` - Guida completa
   - `TODO.md` - Lista implementazioni
   - Commenti nel codice sorgente

3. **Crea il tuo primo template:**
   - Copia `examples/template_ricevuta.html`
   - Modifica HTML/CSS
   - Prova con i tuoi dati

---

## 🎓 Risorse di Apprendimento

### Python Base
- Tutorial ufficiale: https://docs.python.org/it/3/tutorial/
- Python in 10 minuti: https://www.stavros.io/tutorials/python/

### HTML/CSS
- W3Schools: https://www.w3schools.com/html/
- MDN Web Docs: https://developer.mozilla.org/it/docs/Web/HTML

### Jinja2 (Templating)
- Documentazione: https://jinja.palletsprojects.com/
- Tutorial: https://realpython.com/primer-on-jinja-templating/

### ESC/POS
- Epson Manual: https://reference.epson-biz.com/modules/ref_escpos/
- ESC/POS Basics: https://escpos.readthedocs.io/

---

## 💡 Suggerimenti

### 1. Usa Virtual Environment

Sempre! Evita conflitti tra progetti:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Testa Prima con Preview

Salva immagini invece di stampare:
```python
from thermal_printer.templates.renderer import HTMLRenderer

renderer = HTMLRenderer(384)
image = renderer.render_html(your_html)
image.save('preview.png')  # Guarda prima di stampare!
```

### 3. Inizia Semplice

Non partire con template complicati. Inizia con:
```python
printer.print_text("Test", font_size=16, center=True)
```

Poi passa a template HTML man mano che impari.

### 4. Leggi i Commenti

Il codice è commentato al 40%. Leggi i commenti per capire:
```python
# Apri qualsiasi file .py
# Troverai spiegazioni dettagliate
```

### 5. Usa gli Esempi

Gli esempi funzionano! Basta cambiare configurazione:
```python
# In esempio_semplice.py, linea 25
config = PrinterConfig(
    endpoint='192.168.1.100:9100',  # <-- Cambia questo
    # ... resto uguale
)
```

---

## ✨ Sei Pronto!

Ora hai tutto installato e configurato.

**Cosa fare ora:**
1. Esegui `python examples/esempio_semplice.py`
2. Vedi la stampa uscire? 🎉
3. Modifica il codice e sperimenta!

**Domande?**
- Leggi README.md
- Leggi TODO.md
- Guarda i commenti nel codice

**Buona stampa! 🖨️**
