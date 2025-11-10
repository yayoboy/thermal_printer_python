# 🖨️ Thermal Printer App

App Electron con drag & drop builder per stampanti termiche ESC/POS.

## ✨ Caratteristiche

- ✅ **Drag & Drop Builder** - Interfaccia visuale per creare template
- ✅ **Preview 1:1** - Canvas 576px larghezza esatta POS-8370 (80mm)
- ✅ **Template Nunjucks** - Engine di templating (come Jinja2)
- ✅ **HTML → Image** - Rendering con Puppeteer
- ✅ **ESC/POS** - Conversione automatica per stampanti termiche
- ✅ **Multi-connessione** - Supporto Network, USB, Serial
- ✅ **shadcn-ui** - UI moderna e componenti React
- ✅ **TypeScript** - Type-safe development
- ✅ **8 Font Families** - Arial, Times, Courier, Georgia, Verdana, Comic Sans, Impact, Trebuchet
- ✅ **Font Weight Selector** - 9 pesi da Thin (100) a Black (900)
- ✅ **100+ Icone** - Lucide icons organizzate in 12 categorie
- ✅ **Upload Immagini** - Carica file o usa URL
- ✅ **Decoratori** - Box con bordi, colori, padding personalizzabili
- ✅ **Gradient Support** - Gradienti per testi, titoli e sfondi
- ✅ **Color Pickers** - Selezione colori per testi, icone, bordi, gradienti

---

## 🚀 Installazione

### Prerequisiti

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **npm** o **yarn**
- **Stampante termica ESC/POS**

### 1. Installa dipendenze

```bash
cd thermal-printer-app
npm install
```

### 2. Avvia in development

```bash
npm run electron:dev
```

Questo avvierà:
- Vite dev server (React hot reload)
- Electron app

### 3. Build per produzione

```bash
npm run electron:build
```

Troverai l'app compilata in `release/`

---

## 📖 Come usare

### 1️⃣ Configura la stampante

1. Vai su **Impostazioni Stampante**
2. Scegli il tipo di connessione:
   - **Network**: Inserisci IP:porta (es. `192.168.1.100:9100`)
   - **USB**: Seleziona dalla lista dispositivi
   - **Serial**: Seleziona porta COM/ttyUSB
3. Scegli larghezza carta (58mm o 80mm)
4. Clicca **Salva Configurazione**
5. Testa con **Test Stampa**

### 2️⃣ Crea un template

1. Vai su **Template Builder**
2. Trascina componenti dalla palette:
   - **Titolo** - Testo grande con font, peso e colore/gradient personalizzabili
   - **Testo** - Paragrafo con 8 font, 9 pesi, color picker o gradient
   - **Icona** - 100+ icone Lucide organizzate in 12 categorie
   - **Immagine** - Upload file o URL immagine
   - **Tabella** - Dati strutturati in colonne
   - **Separatore** - Linea orizzontale con spessore e colore
   - **Box Decorato** - Contenitore con bordi e background/gradient personalizzabili
   - **Barcode** - Codice a barre simulato
3. Clicca su un componente per modificarne le proprietà:
   - **Font**: Scegli tra 8 famiglie di font
   - **Font Weight**: 9 pesi da Thin (100) a Black (900)
   - **Colore**: Color picker + hex input o Gradient a 2 colori
   - **Gradient**: Direzione (orizzontale, verticale, diagonale)
   - **Allineamento**: Sinistra, centro, destra
   - **Dimensioni**: Font size, padding, bordi
   - **Stili**: Border style, border radius
4. Riordina trascinando i componenti
5. Clicca **Preview** per vedere l'anteprima
6. Clicca **HTML** per vedere il codice generato

### 3️⃣ Salva e stampa

1. Inserisci un nome nel campo "Nome template"
2. Clicca **Salva** per salvare il template
3. Clicca **Stampa** per stampare direttamente

### 4️⃣ Gestisci template salvati

1. Vai su **Template Salvati**
2. Seleziona un template dalla lista
3. Vedi anteprima e codice HTML
4. Esporta come file HTML

---

## 📐 Preview 1:1 - Larghezza Esatta Stampante

Il **Template Builder** mostra un'anteprima **1:1** con la larghezza **esatta** della stampante POS-8370.

### Specifiche Tecniche

- **Larghezza carta**: 80mm
- **Larghezza pixel**: 576px (72 DPI)
- **Area stampabile**: 560px (con margini 8px)
- **Modello**: POS-8370 (compatibile con la maggior parte delle stampanti termiche 80mm)

### Cosa Significa?

✅ **Ciò che vedi è ciò che stampi**: Il canvas ha esattamente 576px di larghezza, la stessa della stampante
✅ **Nessuna sorpresa**: Testi, immagini e layout appariranno identici sulla carta
✅ **Indicatori visivi**: Righelli laterali e label "80mm" per orientarti
✅ **Limiti automatici**: Le immagini sono limitate a max 560px per evitare overflow

### Come Funziona

Il canvas mostra:
- **Bordo carta bianco** - Simula il rotolo di carta termica
- **Area tratteggiata blu** - Area stampabile con padding sicuro
- **Indicatore "Inizio Stampa"** - Mostra dove inizia la stampa
- **Righelli laterali** - Mostrano 0mm e 80mm ai bordi
- **Sfondo grigio** - Simula il tavolo/piano della stampante

### Constraints Automatici

L'app applica automaticamente:
- Larghezza massima immagini: **560px**
- Larghezza totale template: **576px**
- Padding interno: **8-10px** per margini di sicurezza
- Text wrap: Automatico per evitare testi fuori bordo

### Compatibilità

Stampanti termiche supportate:
- ✅ POS-8370 (80mm)
- ✅ Epson TM-T20/T88 (80mm)
- ✅ Star TSP100/650 (80mm)
- ✅ Stampanti ESC/POS generiche 80mm (576px)

**Nota**: Per stampanti 58mm (384px), usa larghezza ridotta (feature futura).

---

## 🎨 Componenti Avanzati

### 📝 Font e Testo

**8 Font disponibili:**
- Arial (sans-serif) - Moderno e pulito
- Times New Roman (serif) - Classico ed elegante
- Courier New (monospace) - Stile typewriter
- Georgia (serif) - Leggibile e professionale
- Verdana (sans-serif) - Ottimo per schermi
- Comic Sans MS (cursive) - Informale
- Impact (fantasy) - Bold e impattante
- Trebuchet MS (sans-serif) - Moderno

**Personalizzazione:**
- Selezione font da dropdown
- **Font Weight**: 9 opzioni da Thin (100) a Black (900)
- Color picker con anteprima o **Gradient** a 2 colori
- Hex color input (#000000 - #ffffff)
- **Direzione Gradient**: Orizzontale, Verticale, Diagonale
- Dimensione font (8px - 72px)
- Allineamento (left/center/right)

### ✨ Icone

**100+ Icone Lucide organizzate in 12 categorie:**
- **Comune**: Heart, Star, Check, X, Plus, Minus, AlertCircle, Info, AlertTriangle, Circle, Square, Triangle
- **Shopping**: ShoppingCart, ShoppingBag, CreditCard, DollarSign, Euro, Tag, Gift, Package, Ticket
- **Comunicazione**: Mail, Phone, MessageCircle, MessageSquare, Send, Inbox, PhoneCall
- **Persone**: User, Users, UserPlus, UserCheck, UserX, Baby, Smile
- **Navigazione**: Home, MapPin, Map, Navigation, Compass, Flag, Target, Arrow (Up/Down/Left/Right)
- **Data & Ora**: Calendar, Clock, Watch, Timer, Hourglass, Sun, Moon
- **Business**: Briefcase, Building, Store, Warehouse, Factory
- **Cibo**: Coffee, Pizza, Wine, Beer, Utensils, Cookie
- **Trasporti**: Truck, Car, Plane, Ship, Bus, Bike, Train
- **Tech**: Settings, Search, Download, Upload, Wifi, Bluetooth, Battery, Power, Zap, Globe
- **Social**: ThumbsUp, ThumbsDown, Award, Trophy, Medal, Crown
- **Altro**: Key, Lock, Eye, Bell, Music, Camera, Image, Film, Book, Bookmark, Newspaper

**Proprietà:**
- Picker visuale con anteprima icone
- Dimensione personalizzabile (8px - 72px)
- Color picker
- Allineamento

### 🖼️ Immagini

**Due modalità di caricamento:**
1. **URL**: Inserisci link immagine (https://...)
2. **Upload File**: Carica da PC (JPG, PNG, GIF, WebP)

**Caratteristiche:**
- Anteprima in tempo reale
- Conversione automatica in base64
- Larghezza massima configurabile
- Testo alternativo (alt)
- Allineamento personalizzabile
- Supporto tutti i formati immagine

### 📦 Box Decorati

**Personalizzazione completa:**
- **Padding**: Spazio interno (0-50px)
- **Bordo**:
  - Spessore (0-10px)
  - Stile: Solido, Tratteggiato, Punteggiato, Doppio
  - Colore con picker
- **Background**: Color picker per sfondo o **Gradient** a 2 colori
- **Direzione Gradient**: Orizzontale, Verticale, Diagonale
- **Border Radius**: Angoli arrotondati (0-20px)

**Casi d'uso:**
- Box promozionali
- Avvisi importanti
- Sezioni evidenziate
- Contenuti speciali

### ➖ Separatori

**Opzioni:**
- Stile: Solido o Tratteggiato
- Spessore: 1-10px
- Colore personalizzabile

---

## 📝 Motore Template Nunjucks

L'app integra **Nunjucks**, un potente motore di templating (equivalente JavaScript di Jinja2) che permette di creare template dinamici con variabili, cicli, condizioni e filtri.

### 🎯 Perché usare i Template?

I template permettono di:
- **Riutilizzare** lo stesso design con dati diversi
- **Automatizzare** la stampa di ricevute, etichette, fatture
- **Generare** documenti dinamici da database o API
- **Personalizzare** contenuti in base ai dati

### 🔧 Sintassi Base

#### Variabili
```nunjucks
{{ nome_variabile }}
{{ prodotto.nome }}
{{ items[0] }}
```

#### Cicli (Loop)
```nunjucks
{% for item in articoli %}
  {{ item.nome }} - € {{ item.prezzo }}
{% endfor %}
```

#### Condizioni (If)
```nunjucks
{% if totale > 100 %}
  <p>Sconto applicato!</p>
{% else %}
  <p>Prezzo standard</p>
{% endif %}
```

#### Filtri
```nunjucks
{{ testo | uppercase }}
{{ prezzo | format_number }}
{{ data | date('DD/MM/YYYY') }}
```

### 📦 Filtri Disponibili

L'app include filtri personalizzati per formattare i dati:

| Filtro | Descrizione | Esempio | Output |
|--------|-------------|---------|--------|
| `uppercase` | Maiuscolo | `{{ "ciao" \| uppercase }}` | `CIAO` |
| `lowercase` | Minuscolo | `{{ "CIAO" \| lowercase }}` | `ciao` |
| `format_number` | Formatta numero | `{{ 1234.56 \| format_number }}` | `1,234.56` |
| `currency` | Formatta valuta | `{{ 10.5 \| currency }}` | `€ 10.50` |
| `truncate` | Tronca testo | `{{ "Testo lungo" \| truncate(5) }}` | `Testo...` |

### 📋 Esempi Pratici

#### Esempio 1: Ricevuta Negozio

**Template HTML:**
```html
<div style="text-align: center; font-family: Arial, sans-serif;">
  <h1 style="font-size: 20px; font-weight: bold;">{{ negozio.nome }}</h1>
  <p style="font-size: 12px;">{{ negozio.indirizzo }}</p>
  <p style="font-size: 12px;">Tel: {{ negozio.telefono }}</p>
</div>

<hr style="border-top: 1px dashed #000; margin: 10px 0;">

<div style="font-size: 12px;">
  <p><strong>Data:</strong> {{ data }}</p>
  <p><strong>Ricevuta N°:</strong> {{ numero_ricevuta }}</p>
</div>

<hr style="border-top: 1px dashed #000; margin: 10px 0;">

<table style="width: 100%; font-size: 12px;">
  {% for item in articoli %}
  <tr>
    <td>{{ item.quantita }}x {{ item.nome }}</td>
    <td style="text-align: right;">{{ item.prezzo | currency }}</td>
  </tr>
  {% endfor %}
</table>

<hr style="border-top: 1px dashed #000; margin: 10px 0;">

<div style="text-align: right; font-size: 14px; font-weight: bold;">
  TOTALE: {{ totale | currency }}
</div>

<div style="text-align: center; margin-top: 20px; font-size: 12px;">
  <p>Grazie per il tuo acquisto!</p>
  {% if punti_fedelta %}
  <p>Hai guadagnato {{ punti_fedelta }} punti fedeltà</p>
  {% endif %}
</div>
```

**Dati JSON:**
```json
{
  "negozio": {
    "nome": "SuperMarket Express",
    "indirizzo": "Via Roma 123, 00100 Roma",
    "telefono": "06 1234567"
  },
  "data": "10/11/2025 - 14:30",
  "numero_ricevuta": "RIC-2025-001234",
  "articoli": [
    { "quantita": 2, "nome": "Latte Intero", "prezzo": 2.50 },
    { "quantita": 1, "nome": "Pane Integrale", "prezzo": 1.80 },
    { "quantita": 3, "nome": "Mele Golden", "prezzo": 4.50 }
  ],
  "totale": 8.80,
  "punti_fedelta": 88
}
```

#### Esempio 2: Etichetta Spedizione

**Template HTML:**
```html
<div style="padding: 10px; font-family: Arial, sans-serif;">
  <div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-size: 24px; font-weight: bold;">SPEDIZIONE</h1>
    <p style="font-size: 16px;">{{ tracking_number }}</p>
  </div>

  <div style="border: 2px solid #000; padding: 10px; margin: 10px 0;">
    <p style="font-size: 10px; margin: 0;"><strong>MITTENTE:</strong></p>
    <p style="font-size: 14px; margin: 5px 0;">{{ mittente.nome }}</p>
    <p style="font-size: 12px; margin: 0;">{{ mittente.indirizzo }}</p>
    <p style="font-size: 12px; margin: 0;">{{ mittente.citta }}, {{ mittente.cap }}</p>
  </div>

  <div style="border: 2px solid #000; padding: 10px; margin: 10px 0;">
    <p style="font-size: 10px; margin: 0;"><strong>DESTINATARIO:</strong></p>
    <p style="font-size: 14px; margin: 5px 0;">{{ destinatario.nome | uppercase }}</p>
    <p style="font-size: 12px; margin: 0;">{{ destinatario.indirizzo }}</p>
    <p style="font-size: 12px; margin: 0;">{{ destinatario.citta }}, {{ destinatario.cap }}</p>
    <p style="font-size: 12px; margin: 5px 0 0 0;">Tel: {{ destinatario.telefono }}</p>
  </div>

  <div style="margin-top: 15px;">
    <p style="font-size: 12px;"><strong>Peso:</strong> {{ peso_kg }} kg</p>
    <p style="font-size: 12px;"><strong>Colli:</strong> {{ numero_colli }}</p>
    <p style="font-size: 12px;"><strong>Tipo:</strong> {{ tipo_servizio }}</p>
  </div>

  {% if note %}
  <div style="margin-top: 10px; padding: 5px; background-color: #ffeb3b;">
    <p style="font-size: 11px; margin: 0;"><strong>Note:</strong> {{ note }}</p>
  </div>
  {% endif %}
</div>
```

**Dati JSON:**
```json
{
  "tracking_number": "IT123456789012",
  "mittente": {
    "nome": "Amazon Logistics",
    "indirizzo": "Via della Logistica 1",
    "citta": "Milano",
    "cap": "20100"
  },
  "destinatario": {
    "nome": "Mario Rossi",
    "indirizzo": "Via Garibaldi 45",
    "citta": "Roma",
    "cap": "00100",
    "telefono": "333 1234567"
  },
  "peso_kg": 2.5,
  "numero_colli": 1,
  "tipo_servizio": "Espresso 24h",
  "note": "Consegnare solo al destinatario"
}
```

#### Esempio 3: Badge Evento/Conferenza

**Template HTML:**
```html
<div style="text-align: center; padding: 15px; font-family: Arial, sans-serif;">
  <div style="background: linear-gradient(to right, #667eea, #764ba2); padding: 20px; color: white; border-radius: 10px;">
    <h1 style="font-size: 22px; margin: 0;">{{ evento.nome }}</h1>
    <p style="font-size: 14px; margin: 5px 0;">{{ evento.data }}</p>
  </div>

  <div style="margin: 20px 0;">
    <h2 style="font-size: 28px; margin: 10px 0;">{{ partecipante.nome | uppercase }}</h2>
    <p style="font-size: 16px; color: #666; margin: 5px 0;">{{ partecipante.azienda }}</p>
  </div>

  <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin: 10px 0;">
    <p style="font-size: 18px; font-weight: bold; margin: 0;">{{ partecipante.tipologia | uppercase }}</p>
  </div>

  <div style="margin-top: 15px; font-size: 12px; color: #666;">
    <p>Badge ID: {{ partecipante.badge_id }}</p>
    {% if partecipante.accesso_vip %}
    <p style="color: #d4af37; font-weight: bold;">★ ACCESSO VIP ★</p>
    {% endif %}
  </div>

  <div style="margin-top: 20px; font-size: 10px; color: #999;">
    <p>{{ evento.luogo }}</p>
    <p>Ore: {{ evento.orario_inizio }} - {{ evento.orario_fine }}</p>
  </div>
</div>
```

**Dati JSON:**
```json
{
  "evento": {
    "nome": "Tech Summit 2025",
    "data": "15-16 Novembre 2025",
    "luogo": "Milano Convention Center",
    "orario_inizio": "09:00",
    "orario_fine": "18:00"
  },
  "partecipante": {
    "nome": "Laura Bianchi",
    "azienda": "TechCorp Italia",
    "tipologia": "Speaker",
    "badge_id": "TS2025-SPK-042",
    "accesso_vip": true
  }
}
```

### 🚀 Come Usare i Template

#### Metodo 1: Template Builder (GUI)

1. Vai su **Template Builder**
2. Crea il design visualmente con drag & drop
3. Clicca **HTML** per vedere il codice
4. Copia il codice e sostituisci i valori fissi con variabili Nunjucks
5. Salva il template modificato

#### Metodo 2: Da Codice JavaScript/TypeScript

```typescript
// Renderizza template con dati
const html = await window.electronAPI.template.render(templateString, dati)

// Stampa direttamente
await window.electronAPI.printer.printTemplate(templateString, dati, 384)

// Esempio completo
const template = `
<div style="text-align: center;">
  <h1>{{ titolo }}</h1>
  {% for item in items %}
  <p>{{ item }}</p>
  {% endfor %}
</div>
`

const dati = {
  titolo: "Lista Prodotti",
  items: ["Prodotto 1", "Prodotto 2", "Prodotto 3"]
}

await window.electronAPI.printer.printTemplate(template, dati, 384)
```

#### Metodo 3: Caricare Template Salvati

```typescript
// Carica template salvato
const result = await window.electronAPI.template.load('ricevuta_negozio')
const template = result.content

// Renderizza con nuovi dati
const html = await window.electronAPI.template.render(template, nuoviDati)
```

### 💡 Tips & Best Practices

1. **Usa variabili descrittive**: `{{ prodotto.nome }}` invece di `{{ p.n }}`
2. **Gestisci valori mancanti**: Usa `{% if variabile %}...{% endif %}`
3. **Formatta i numeri**: Usa sempre i filtri `format_number` o `currency`
4. **Testa con dati reali**: Assicurati che il template funzioni con tutti i casi
5. **Mantieni HTML semplice**: Le stampanti termiche hanno capacità limitate
6. **Evita CSS complessi**: Usa solo stili inline e proprietà base
7. **Dimensioni font**: Usa font 10-14px per testo normale, 16-24px per titoli

### 🔗 Risorse

- **Nunjucks Docs**: https://mozilla.github.io/nunjucks/
- **Tutti i tag**: https://mozilla.github.io/nunjucks/templating.html#tags
- **Tutti i filtri built-in**: https://mozilla.github.io/nunjucks/templating.html#filters

---

## 🏗️ Architettura

```
thermal-printer-app/
├── src/
│   ├── main/                    # Electron Main Process
│   │   ├── main.ts             # Entry point Electron
│   │   ├── preload.ts          # Bridge sicuro per IPC
│   │   └── services/           # Backend services
│   │       ├── TemplateService.ts    # Nunjucks engine
│   │       ├── RenderService.ts      # HTML → Image (Puppeteer)
│   │       └── PrinterService.ts     # ESC/POS printing
│   │
│   └── renderer/               # React Frontend
│       ├── main.tsx           # Entry point React
│       ├── App.tsx            # App principale
│       ├── components/        # Componenti React
│       │   ├── ui/           # shadcn-ui components
│       │   ├── builder/      # Drag & Drop builder
│       │   ├── TemplateBuilder.tsx
│       │   ├── PrinterSettings.tsx
│       │   └── TemplateManager.tsx
│       └── styles/
│           └── globals.css    # TailwindCSS
│
├── package.json
├── vite.config.ts
├── tsconfig.json
└── tailwind.config.js
```

---

## 🔧 Tecnologie

### Frontend
- **Electron** - Desktop app framework
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **TailwindCSS v4** - Styling
- **shadcn-ui** - UI components
- **@dnd-kit** - Drag & drop

### Backend (Main Process)
- **Nunjucks** - Template engine
- **Puppeteer** - HTML → Image rendering
- **escpos** + adapters - ESC/POS printing
- **serialport** - Serial communication
- **usb** - USB communication

---

## 📝 API IPC

L'app usa IPC (Inter-Process Communication) per comunicare tra frontend e backend.

### Template API

```typescript
// Renderizza template con dati
window.electronAPI.template.render(template: string, data: any)

// Salva template
window.electronAPI.template.save(name: string, content: string)

// Carica template
window.electronAPI.template.load(name: string)

// Lista template
window.electronAPI.template.list()
```

### Render API

```typescript
// Converti HTML in immagine
window.electronAPI.render.htmlToImage(html: string, width: number)
```

### Printer API

```typescript
// Lista stampanti
window.electronAPI.printer.list(type: 'network' | 'usb' | 'serial')

// Configura stampante
window.electronAPI.printer.configure(config: PrinterConfig)

// Stampa immagine
window.electronAPI.printer.printImage(imageBase64: string)

// Stampa HTML
window.electronAPI.printer.printHtml(html: string, width: number)

// Stampa template
window.electronAPI.printer.printTemplate(template: string, data: any, width: number)

// Test
window.electronAPI.printer.test()
```

---

## 🎨 Personalizzazione

### Aggiungi nuovi componenti

1. Apri `src/renderer/components/TemplateBuilder.tsx`
2. Aggiungi il tipo in `ComponentType`
3. Implementa rendering in `generateHTML()`
4. Aggiungi alla palette in `ComponentPalette.tsx`
5. Aggiungi proprietà in `ComponentProperties.tsx`

### Modifica stili template

Modifica `TemplateService.ts` → `createFullHtml()` per cambiare gli stili base.

### Aggiungi filtri Nunjucks

Modifica `TemplateService.ts` → `setupFilters()`:

```typescript
this.env.addFilter('mio_filtro', (value: any) => {
  // La tua logica
  return transformed_value
})
```

---

## 🐛 Troubleshooting

### Stampante non si connette

**Network:**
- Verifica IP con `ping 192.168.1.100`
- Controlla che la porta 9100 sia aperta
- Assicurati di essere sulla stessa rete

**USB:**
- Su Linux, serve permesso:
  ```bash
  sudo usermod -a -G lp $USER
  ```
- Riavvia dopo aver aggiunto al gruppo

**Serial:**
- Su Linux, serve permesso dialout:
  ```bash
  sudo usermod -a -G dialout $USER
  ```

### Puppeteer non trova Chrome

**Linux:**
```bash
sudo apt install chromium-browser
```

**macOS:**
```bash
brew install chromium
```

**Windows:**
Installa Google Chrome da https://www.google.com/chrome/

### Errori di build

```bash
# Pulisci e reinstalla
rm -rf node_modules package-lock.json
npm install
```

### App non si avvia in dev mode

Verifica che la porta 5173 sia libera:
```bash
lsof -i :5173  # Mac/Linux
netstat -ano | findstr :5173  # Windows
```

---

## 🤝 Contribuire

Contributi benvenuti! Sentiti libero di:
- Aprire issue per bug o feature request
- Fare PR con miglioramenti
- Aggiungere nuovi componenti per il builder
- Migliorare la documentazione

---

## 📄 Licenza

MIT License - Usa liberamente per progetti personali e commerciali.

---

## 🎓 Risorse

### Documentazione
- [Electron](https://www.electronjs.org/docs)
- [React](https://react.dev/)
- [Nunjucks](https://mozilla.github.io/nunjucks/)
- [Puppeteer](https://pptr.dev/)
- [node-escpos](https://github.com/lsongdev/node-escpos)
- [shadcn-ui](https://ui.shadcn.com/)

### ESC/POS
- [Epson ESC/POS Command Reference](https://reference.epson-biz.com/modules/ref_escpos/)

---

## 💡 Esempi d'uso

### Template ricevuta negozio

```nunjucks
<div style="text-align: center;">
  <h1>{{ negozio.nome }}</h1>
  <p>{{ negozio.indirizzo }}</p>
  <p>Tel: {{ negozio.telefono }}</p>
</div>

<hr style="border-top: 1px dashed #000; margin: 10px 0;">

<table style="width: 100%;">
  {% for item in articoli %}
  <tr>
    <td>{{ item.nome }}</td>
    <td style="text-align: right;">€ {{ item.prezzo|format_number }}</td>
  </tr>
  {% endfor %}
</table>

<hr style="border-top: 1px dashed #000; margin: 10px 0;">

<div style="text-align: right; font-weight: bold;">
  TOTALE: € {{ totale|format_number }}
</div>

<div style="text-align: center; margin-top: 20px;">
  <p>Grazie per il tuo acquisto!</p>
</div>
```

### Usa nel codice

```typescript
const data = {
  negozio: {
    nome: "Il Mio Negozio",
    indirizzo: "Via Roma 1, 00100 Roma",
    telefono: "06 1234567"
  },
  articoli: [
    { nome: "Prodotto 1", prezzo: 10.50 },
    { nome: "Prodotto 2", prezzo: 25.00 }
  ],
  totale: 35.50
}

await window.electronAPI.printer.printTemplate(template, data, 384)
```

---

**Buona stampa! 🖨️✨**
