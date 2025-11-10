# 🖨️ Thermal Printer App

App Electron con drag & drop builder per stampanti termiche ESC/POS.

## ✨ Caratteristiche

- ✅ **Drag & Drop Builder** - Interfaccia visuale per creare template
- ✅ **Template Nunjucks** - Engine di templating (come Jinja2)
- ✅ **HTML → Image** - Rendering con Puppeteer
- ✅ **ESC/POS** - Conversione automatica per stampanti termiche
- ✅ **Multi-connessione** - Supporto Network, USB, Serial
- ✅ **shadcn-ui** - UI moderna e componenti React
- ✅ **TypeScript** - Type-safe development

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
   - **Titolo** - Testo grande in grassetto
   - **Testo** - Paragrafo normale
   - **Tabella** - Dati strutturati
   - **Separatore** - Linea orizzontale
   - **Barcode** - Codice a barre simulato
3. Clicca su un componente per modificarne le proprietà
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
