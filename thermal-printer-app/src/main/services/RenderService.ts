import puppeteer, { Browser, Page } from 'puppeteer'

/**
 * Service per convertire HTML in immagini
 * Equivalente al HTMLRenderer di Python ma usando Puppeteer
 */
export class RenderService {
  private browser: Browser | null = null

  /**
   * Inizializza il browser Puppeteer
   */
  private async initBrowser(): Promise<Browser> {
    if (!this.browser) {
      this.browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      })
    }
    return this.browser
  }

  /**
   * Converte HTML in immagine PNG
   *
   * @param html - Contenuto HTML da renderizzare
   * @param width - Larghezza dell'immagine in pixel (384 per 58mm, 576 per 80mm)
   * @returns Buffer contenente l'immagine PNG
   */
  async htmlToImage(html: string, width: number = 384): Promise<Buffer> {
    let page: Page | null = null

    try {
      // Inizializza browser
      const browser = await this.initBrowser()

      // Crea nuova pagina
      page = await browser.newPage()

      // Imposta viewport (larghezza fissa, altezza si adatta)
      await page.setViewport({
        width: width,
        height: 100, // Minimo, si espanderà
        deviceScaleFactor: 1,
      })

      // Carica l'HTML
      await page.setContent(html, {
        waitUntil: 'networkidle0', // Aspetta che tutto sia caricato
      })

      // Ottieni l'altezza effettiva del contenuto
      const bodyHeight = await page.evaluate(() => {
        return document.body.scrollHeight
      })

      // Aggiorna viewport con altezza corretta
      await page.setViewport({
        width: width,
        height: bodyHeight,
        deviceScaleFactor: 1,
      })

      // Cattura screenshot
      const screenshot = await page.screenshot({
        type: 'png',
        fullPage: true,
        omitBackground: false, // Sfondo bianco
      })

      return screenshot as Buffer

    } catch (error: any) {
      throw new Error(`HTML to Image conversion failed: ${error.message}`)
    } finally {
      // Chiudi la pagina
      if (page) {
        await page.close()
      }
    }
  }

  /**
   * Chiude il browser
   */
  async close(): Promise<void> {
    if (this.browser) {
      await this.browser.close()
      this.browser = null
    }
  }

  /**
   * Converte HTML con stili inline (utile per template semplici)
   */
  async simpleHtmlToImage(
    content: string,
    width: number = 384,
    styles: string = ''
  ): Promise<Buffer> {
    const html = `
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
      font-family: Arial, sans-serif;
      background: white;
      padding: 10px;
    }
    ${styles}
  </style>
</head>
<body>
  ${content}
</body>
</html>
    `

    return this.htmlToImage(html, width)
  }

  /**
   * Renderizza testo semplice come immagine
   */
  async textToImage(
    text: string,
    width: number = 384,
    options: {
      fontSize?: number
      fontWeight?: string
      textAlign?: string
      padding?: number
    } = {}
  ): Promise<Buffer> {
    const {
      fontSize = 12,
      fontWeight = 'normal',
      textAlign = 'left',
      padding = 10,
    } = options

    const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      width: ${width}px;
      font-family: Arial, sans-serif;
      font-size: ${fontSize}px;
      font-weight: ${fontWeight};
      text-align: ${textAlign};
      padding: ${padding}px;
      margin: 0;
      background: white;
      color: black;
    }
  </style>
</head>
<body>${text}</body>
</html>
    `

    return this.htmlToImage(html, width)
  }
}
