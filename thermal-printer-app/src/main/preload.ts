import { contextBridge, ipcRenderer } from 'electron'

/**
 * Preload script che espone API sicure al renderer process
 * Usa contextBridge per creare un bridge tra Electron e React
 */

// Definisci le API esposte
const api = {
  // Template operations
  template: {
    render: (template: string, data: any) =>
      ipcRenderer.invoke('template:render', template, data),

    save: (name: string, content: string) =>
      ipcRenderer.invoke('template:save', name, content),

    load: (name: string) =>
      ipcRenderer.invoke('template:load', name),

    list: () =>
      ipcRenderer.invoke('template:list'),
  },

  // Render operations
  render: {
    htmlToImage: (html: string, width: number) =>
      ipcRenderer.invoke('render:html-to-image', html, width),
  },

  // Printer operations
  printer: {
    list: (type: 'network' | 'usb' | 'serial') =>
      ipcRenderer.invoke('printer:list', type),

    configure: (config: any) =>
      ipcRenderer.invoke('printer:configure', config),

    printImage: (imageBase64: string) =>
      ipcRenderer.invoke('printer:print-image', imageBase64),

    printHtml: (html: string, width: number) =>
      ipcRenderer.invoke('printer:print-html', html, width),

    printTemplate: (template: string, data: any, width: number) =>
      ipcRenderer.invoke('printer:print-template', template, data, width),

    test: () =>
      ipcRenderer.invoke('printer:test'),
  },
}

// Esponi l'API al renderer process
contextBridge.exposeInMainWorld('electronAPI', api)

// Type definition for TypeScript
export type ElectronAPI = typeof api
