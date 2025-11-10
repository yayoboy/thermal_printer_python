// @ts-ignore - escpos non ha types ufficiali
import escpos from 'escpos'
// @ts-ignore - escpos adapters non hanno types completi
import USB from 'escpos-usb'
// @ts-ignore
import Network from 'escpos-network'
// @ts-ignore
import Serial from 'escpos-serialport'
import { SerialPort } from 'serialport'
import usb from 'usb'

// Assegna gli adapter a escpos
escpos.USB = USB
escpos.Network = Network
escpos.Serial = Serial

/**
 * Configurazione stampante
 */
export interface PrinterConfig {
  type: 'network' | 'usb' | 'serial'
  endpoint?: string // IP:porta per network, path per serial
  vendorId?: number // Per USB
  productId?: number // Per USB
  width?: number // Larghezza in pixel (384 o 576)
}

/**
 * Service per gestire la stampa ESC/POS
 * Equivalente ai backend di stampa di Python
 */
export class PrinterService {
  private config: PrinterConfig | null = null
  private device: any = null
  private printer: escpos.Printer | null = null

  /**
   * Configura la stampante
   */
  async configure(config: PrinterConfig): Promise<void> {
    this.config = config

    // Chiudi connessione esistente se presente
    if (this.device) {
      try {
        await this.disconnect()
      } catch (error) {
        // Ignora errori di disconnessione
      }
    }

    // Crea nuovo device in base al tipo
    switch (config.type) {
      case 'network':
        if (!config.endpoint) {
          throw new Error('Network printer requires endpoint (IP:port)')
        }
        const [host, portStr] = config.endpoint.split(':')
        const port = parseInt(portStr) || 9100
        this.device = new Network(host, port)
        break

      case 'usb':
        if (!config.vendorId || !config.productId) {
          throw new Error('USB printer requires vendorId and productId')
        }
        this.device = new USB(config.vendorId, config.productId)
        break

      case 'serial':
        if (!config.endpoint) {
          throw new Error('Serial printer requires endpoint (port path)')
        }
        this.device = new Serial(config.endpoint, {
          baudRate: 9600,
          autoOpen: false,
        })
        break

      default:
        throw new Error(`Unknown printer type: ${config.type}`)
    }
  }

  /**
   * Connetti alla stampante
   */
  private async connect(): Promise<void> {
    if (!this.device) {
      throw new Error('Printer not configured')
    }

    return new Promise((resolve, reject) => {
      this.device.open((error: Error | null) => {
        if (error) {
          reject(new Error(`Failed to connect to printer: ${error.message}`))
        } else {
          this.printer = new escpos.Printer(this.device, {
            encoding: 'UTF-8',
          })
          resolve()
        }
      })
    })
  }

  /**
   * Disconnetti dalla stampante
   */
  private async disconnect(): Promise<void> {
    if (this.device) {
      return new Promise((resolve) => {
        this.device.close(() => {
          this.printer = null
          resolve()
        })
      })
    }
  }

  /**
   * Stampa un'immagine (da Buffer)
   */
  async printImage(imageBuffer: Buffer): Promise<void> {
    if (!this.config) {
      throw new Error('Printer not configured')
    }

    try {
      // Connetti alla stampante
      await this.connect()

      if (!this.printer) {
        throw new Error('Printer not initialized')
      }

      // Crea un promise per la stampa
      return new Promise((resolve, reject) => {
        try {
          // Inizializza stampante
          this.printer!
            .align('CT')
            .image(imageBuffer, 's8') // s8 = doppia densità
            .feed(3) // Avanza carta
            .cut() // Taglia carta
            .close(() => {
              this.disconnect().then(resolve).catch(reject)
            })
        } catch (error: any) {
          reject(new Error(`Print failed: ${error.message}`))
        }
      })
    } catch (error: any) {
      await this.disconnect()
      throw error
    }
  }

  /**
   * Stampa di test
   */
  async testPrint(): Promise<void> {
    if (!this.config) {
      throw new Error('Printer not configured')
    }

    try {
      await this.connect()

      if (!this.printer) {
        throw new Error('Printer not initialized')
      }

      return new Promise((resolve, reject) => {
        try {
          this.printer!
            .align('CT')
            .style('B')
            .size(2, 2)
            .text('TEST STAMPA')
            .style('NORMAL')
            .size(1, 1)
            .text('\n')
            .text('Thermal Printer App')
            .text('\n')
            .text('━━━━━━━━━━━━━━━━━━━━')
            .text('\n')
            .align('LT')
            .text('Stampante configurata correttamente!')
            .text('\n')
            .text(`Tipo: ${this.config.type}`)
            .text('\n')
            .text(`Larghezza: ${this.config.width || 384}px`)
            .text('\n')
            .feed(3)
            .cut()
            .close(() => {
              this.disconnect().then(resolve).catch(reject)
            })
        } catch (error: any) {
          reject(new Error(`Test print failed: ${error.message}`))
        }
      })
    } catch (error: any) {
      await this.disconnect()
      throw error
    }
  }

  /**
   * Lista stampanti USB disponibili
   */
  async listUsbPrinters(): Promise<Array<{ vendorId: number; productId: number; name: string }>> {
    const devices = usb.getDeviceList()
    const printers: Array<{ vendorId: number; productId: number; name: string }> = []

    for (const device of devices) {
      // Filtra solo dispositivi che potrebbero essere stampanti
      // Class 7 = Printer
      const descriptor = device.deviceDescriptor

      // Cerca stampanti termiche comuni
      if (
        descriptor.bDeviceClass === 7 || // Printer class
        descriptor.bDeviceClass === 0 // Check interfaces
      ) {
        printers.push({
          vendorId: descriptor.idVendor,
          productId: descriptor.idProduct,
          name: `USB Printer ${descriptor.idVendor.toString(16)}:${descriptor.idProduct.toString(16)}`,
        })
      }
    }

    return printers
  }

  /**
   * Lista porte seriali disponibili
   */
  async listSerialPorts(): Promise<Array<{ path: string; manufacturer?: string }>> {
    const ports = await SerialPort.list()
    return ports.map((port) => ({
      path: port.path,
      manufacturer: port.manufacturer,
    }))
  }

  /**
   * Lista stampanti in base al tipo
   */
  async listPrinters(type: 'network' | 'usb' | 'serial'): Promise<any[]> {
    switch (type) {
      case 'usb':
        return this.listUsbPrinters()
      case 'serial':
        return this.listSerialPorts()
      case 'network':
        // Network discovery richiederebbe mDNS/Bonjour
        // Per semplicità, ritorniamo un array vuoto
        // L'utente dovrà inserire IP manualmente
        return []
      default:
        return []
    }
  }
}
