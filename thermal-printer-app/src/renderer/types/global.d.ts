/**
 * Type definitions per window.electronAPI
 */

export interface ElectronAPI {
  template: {
    render: (template: string, data: any) => Promise<{ success: boolean; html?: string; error?: string }>
    save: (name: string, content: string) => Promise<{ success: boolean; error?: string }>
    load: (name: string) => Promise<{ success: boolean; content?: string; error?: string }>
    list: () => Promise<{ success: boolean; templates?: string[]; error?: string }>
  }
  render: {
    htmlToImage: (html: string, width: number) => Promise<{ success: boolean; image?: string; error?: string }>
  }
  printer: {
    list: (type: 'network' | 'usb' | 'serial') => Promise<{ success: boolean; printers?: any[]; error?: string }>
    configure: (config: any) => Promise<{ success: boolean; error?: string }>
    printImage: (imageBase64: string) => Promise<{ success: boolean; error?: string }>
    printHtml: (html: string, width: number) => Promise<{ success: boolean; error?: string }>
    printTemplate: (template: string, data: any, width: number) => Promise<{ success: boolean; error?: string }>
    test: () => Promise<{ success: boolean; error?: string }>
  }
}

declare global {
  interface Window {
    electronAPI: ElectronAPI
  }
}

export {}
