import nunjucks from 'nunjucks'
import fs from 'fs/promises'
import path from 'path'
import { app } from 'electron'

/**
 * Service per gestire i template Nunjucks
 * Equivalente al TemplateEngine di Python ma in JavaScript
 */
export class TemplateService {
  private env: nunjucks.Environment
  private templatesPath: string

  constructor() {
    // Path dove salvare i template
    this.templatesPath = path.join(app.getPath('userData'), 'templates')

    // Configura Nunjucks
    this.env = nunjucks.configure(this.templatesPath, {
      autoescape: true,
      trimBlocks: true,
      lstripBlocks: true,
    })

    // Aggiungi filtri custom (come in Python)
    this.setupFilters()

    // Crea la directory se non esiste
    this.ensureTemplatesDir()
  }

  /**
   * Setup filtri personalizzati (equivalenti a quelli Python)
   */
  private setupFilters() {
    // Filtro uppercase
    this.env.addFilter('uppercase', (str: string) => {
      return str.toUpperCase()
    })

    // Filtro lowercase
    this.env.addFilter('lowercase', (str: string) => {
      return str.toLowerCase()
    })

    // Filtro per formattare numeri (es. prezzi)
    this.env.addFilter('format_number', (num: number, decimals = 2) => {
      return num.toFixed(decimals)
    })

    // Filtro per formattare valuta
    this.env.addFilter('currency', (num: number, symbol = '€') => {
      return `${symbol} ${num.toFixed(2)}`
    })

    // Filtro per troncare testo
    this.env.addFilter('truncate', (str: string, length: number) => {
      if (str.length <= length) return str
      return str.substring(0, length) + '...'
    })
  }

  /**
   * Assicura che la directory template esista
   */
  private async ensureTemplatesDir() {
    try {
      await fs.mkdir(this.templatesPath, { recursive: true })
    } catch (error) {
      console.error('Error creating templates directory:', error)
    }
  }

  /**
   * Renderizza un template da stringa con dati
   */
  render(template: string, data: any): string {
    try {
      return this.env.renderString(template, data)
    } catch (error: any) {
      throw new Error(`Template render error: ${error.message}`)
    }
  }

  /**
   * Renderizza un template da file
   */
  async renderFromFile(filename: string, data: any): Promise<string> {
    try {
      const template = await this.loadTemplate(filename)
      return this.render(template, data)
    } catch (error: any) {
      throw new Error(`Template file render error: ${error.message}`)
    }
  }

  /**
   * Salva un template su file
   */
  async saveTemplate(name: string, content: string): Promise<void> {
    const filePath = path.join(this.templatesPath, `${name}.html`)
    await fs.writeFile(filePath, content, 'utf-8')
  }

  /**
   * Carica un template da file
   */
  async loadTemplate(name: string): Promise<string> {
    const filePath = path.join(this.templatesPath, `${name}.html`)
    return await fs.readFile(filePath, 'utf-8')
  }

  /**
   * Lista tutti i template salvati
   */
  async listTemplates(): Promise<string[]> {
    try {
      const files = await fs.readdir(this.templatesPath)
      return files
        .filter(file => file.endsWith('.html'))
        .map(file => file.replace('.html', ''))
    } catch (error) {
      return []
    }
  }

  /**
   * Elimina un template
   */
  async deleteTemplate(name: string): Promise<void> {
    const filePath = path.join(this.templatesPath, `${name}.html`)
    await fs.unlink(filePath)
  }

  /**
   * Crea HTML completo con stili base per stampa termica
   */
  createFullHtml(content: string, width: number = 384): string {
    return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      width: ${width}px;
      font-family: 'Arial', sans-serif;
      font-size: 12px;
      line-height: 1.4;
      color: #000;
      background: #fff;
      padding: 10px;
    }
    h1 {
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 10px;
      text-align: center;
    }
    h2 {
      font-size: 16px;
      font-weight: bold;
      margin-bottom: 8px;
    }
    h3 {
      font-size: 14px;
      font-weight: bold;
      margin-bottom: 6px;
    }
    p {
      margin-bottom: 8px;
    }
    hr {
      border: none;
      border-top: 1px dashed #000;
      margin: 10px 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 10px;
    }
    td, th {
      padding: 4px;
      text-align: left;
    }
    .center {
      text-align: center;
    }
    .right {
      text-align: right;
    }
    .bold {
      font-weight: bold;
    }
    .barcode {
      text-align: center;
      font-family: 'Courier New', monospace;
      letter-spacing: 2px;
      margin: 10px 0;
    }
  </style>
</head>
<body>
  ${content}
</body>
</html>
    `.trim()
  }
}
