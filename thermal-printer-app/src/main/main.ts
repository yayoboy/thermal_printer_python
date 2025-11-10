import { app, BrowserWindow, ipcMain } from 'electron'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Importa i servizi
import { TemplateService } from './services/TemplateService'
import { RenderService } from './services/RenderService'
import { PrinterService } from './services/PrinterService'

let mainWindow: BrowserWindow | null = null

// Servizi globali
const templateService = new TemplateService()
const renderService = new RenderService()
const printerService = new PrinterService()

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
    title: 'Thermal Printer - Drag & Drop Builder'
  })

  // In development mode, load from Vite dev server
  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL)
    mainWindow.webContents.openDevTools()
  } else {
    // In production, load the built files
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// App ready
app.whenReady().then(() => {
  createWindow()
  setupIpcHandlers()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

// Quit when all windows are closed
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// IPC Handlers
function setupIpcHandlers() {

  // ==========================================
  // TEMPLATE RENDERING
  // ==========================================

  /**
   * Renderizza un template Nunjucks con i dati forniti
   */
  ipcMain.handle('template:render', async (event, template: string, data: any) => {
    try {
      const html = templateService.render(template, data)
      return { success: true, html }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  /**
   * Salva un template su file
   */
  ipcMain.handle('template:save', async (event, name: string, content: string) => {
    try {
      await templateService.saveTemplate(name, content)
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  /**
   * Carica un template da file
   */
  ipcMain.handle('template:load', async (event, name: string) => {
    try {
      const content = await templateService.loadTemplate(name)
      return { success: true, content }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  /**
   * Lista tutti i template salvati
   */
  ipcMain.handle('template:list', async () => {
    try {
      const templates = await templateService.listTemplates()
      return { success: true, templates }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  // ==========================================
  // HTML TO IMAGE RENDERING
  // ==========================================

  /**
   * Converte HTML in immagine PNG
   */
  ipcMain.handle('render:html-to-image', async (event, html: string, width: number) => {
    try {
      const imageBuffer = await renderService.htmlToImage(html, width)
      return { success: true, image: imageBuffer.toString('base64') }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  // ==========================================
  // PRINTER OPERATIONS
  // ==========================================

  /**
   * Lista le stampanti disponibili
   */
  ipcMain.handle('printer:list', async (event, type: 'network' | 'usb' | 'serial') => {
    try {
      const printers = await printerService.listPrinters(type)
      return { success: true, printers }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  /**
   * Configura la stampante
   */
  ipcMain.handle('printer:configure', async (event, config: any) => {
    try {
      await printerService.configure(config)
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  /**
   * Stampa un'immagine (base64) sulla stampante configurata
   */
  ipcMain.handle('printer:print-image', async (event, imageBase64: string) => {
    try {
      const imageBuffer = Buffer.from(imageBase64, 'base64')
      await printerService.printImage(imageBuffer)
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  /**
   * Stampa direttamente HTML (combina render + print)
   */
  ipcMain.handle('printer:print-html', async (event, html: string, width: number) => {
    try {
      // 1. Converti HTML in immagine
      const imageBuffer = await renderService.htmlToImage(html, width)

      // 2. Stampa l'immagine
      await printerService.printImage(imageBuffer)

      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  /**
   * Stampa un template con dati (render template + html to image + print)
   */
  ipcMain.handle('printer:print-template', async (event, template: string, data: any, width: number) => {
    try {
      // 1. Renderizza template
      const html = templateService.render(template, data)

      // 2. Converti in immagine
      const imageBuffer = await renderService.htmlToImage(html, width)

      // 3. Stampa
      await printerService.printImage(imageBuffer)

      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })

  /**
   * Test di stampa
   */
  ipcMain.handle('printer:test', async () => {
    try {
      await printerService.testPrint()
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  })
}
