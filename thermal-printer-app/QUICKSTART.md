# 🚀 Quick Start - Thermal Printer App

Guida rapida per iniziare in 5 minuti!

## 1️⃣ Installazione (2 minuti)

```bash
# Entra nella cartella
cd thermal-printer-app

# Installa dipendenze
npm install
```

## 2️⃣ Avvia l'app (30 secondi)

```bash
npm run electron:dev
```

Aspetta che si apra l'applicazione Electron.

## 3️⃣ Configura stampante (1 minuto)

1. Vai alla tab **"Impostazioni Stampante"**

2. Scegli il tipo di connessione:

   **Stampante Network (WiFi/Ethernet):**
   - Seleziona "Network"
   - Inserisci IP della stampante (es. `192.168.1.100`)
   - Porta: `9100` (default)

   **Stampante USB:**
   - Seleziona "USB"
   - Clicca "Aggiorna Lista"
   - Seleziona la tua stampante dalla lista

   **Stampante Serial (COM/ttyUSB):**
   - Seleziona "Seriale"
   - Clicca "Aggiorna Lista"
   - Seleziona la porta dalla lista

3. Scegli larghezza:
   - **58mm (384px)** - stampanti piccole
   - **80mm (576px)** - stampanti standard

4. Clicca **"Salva Configurazione"**

5. Clicca **"Test Stampa"** per verificare

## 4️⃣ Crea il tuo primo template (2 minuti)

1. Vai alla tab **"Template Builder"**

2. Trascina componenti dalla palette di sinistra:
   - **Titolo** → trascina nel canvas
   - Clicca sul titolo per modificarlo nel pannello destro
   - Cambia testo in "Il Mio Negozio"

3. Aggiungi altri componenti:
   - **Separatore** (linea orizzontale)
   - **Testo** (descrizione)
   - **Tabella** (per prodotti e prezzi)

4. Modifica proprietà:
   - Clicca su un componente
   - Modifica nel pannello destro
   - Cambia allineamento, dimensione, contenuto

5. Clicca **"Preview"** per vedere l'anteprima

6. Inserisci nome: `mio-primo-template`

7. Clicca **"Salva"**

8. Clicca **"Stampa"** 🎉

## 5️⃣ Usa template salvati

1. Vai alla tab **"Template Salvati"**
2. Vedi la lista dei template
3. Clicca su un template per visualizzarlo
4. Esporta come HTML se necessario

---

## 🎯 Prossimi passi

### Usa variabili dinamiche

I template supportano Nunjucks (come Jinja2):

```html
<h1>Ciao {{ nome }}!</h1>
<p>Totale: € {{ prezzo|format_number }}</p>
```

### Crea template avanzati

Vedi `templates/ricevuta-esempio.html` per un esempio completo di ricevuta con:
- Intestazione negozio
- Tabella articoli
- Calcoli IVA
- Footer

### Usa l'API

Se vuoi integrare in un'altra app:

```typescript
// Stampa template con dati
await window.electronAPI.printer.printTemplate(
  templateHTML,
  {
    negozio: { nome: "Il Mio Shop" },
    articoli: [
      { nome: "Prodotto 1", prezzo: 10.50 }
    ],
    totale: 10.50
  },
  384  // larghezza in px
)
```

---

## 🐛 Problemi comuni

### "Stampante non trovata"
→ Verifica IP/connessione e riesegui configurazione

### "Chrome/Chromium not found" (Puppeteer)
→ Installa Chrome o Chromium sul sistema

### "Permission denied" (USB/Serial su Linux)
→ Aggiungi utente ai gruppi:
```bash
sudo usermod -a -G lp,dialout $USER
```
→ Riavvia

### Porta 5173 già in uso
→ Chiudi altre app Vite o cambia porta in `vite.config.ts`

---

## 📖 Documentazione completa

Vedi `README.md` per la guida completa.

---

**Buon divertimento! 🖨️✨**
