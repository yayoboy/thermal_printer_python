import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Printer, Wifi, Usb, Cable, CheckCircle2 } from 'lucide-react'

type PrinterType = 'network' | 'usb' | 'serial'

export function PrinterSettings() {
  const [printerType, setPrinterType] = useState<PrinterType>('network')
  const [networkIp, setNetworkIp] = useState('192.168.1.100')
  const [networkPort, setNetworkPort] = useState('9100')
  const [printerWidth, setPrinterWidth] = useState('384')
  const [usbDevices, setUsbDevices] = useState<any[]>([])
  const [serialPorts, setSerialPorts] = useState<any[]>([])
  const [selectedUsb, setSelectedUsb] = useState<{ vendorId: number; productId: number } | null>(null)
  const [selectedSerial, setSelectedSerial] = useState<string>('')
  const [status, setStatus] = useState<string>('')
  const [testing, setTesting] = useState(false)

  // Carica lista dispositivi quando cambia il tipo
  useEffect(() => {
    if (printerType === 'usb') {
      loadUsbDevices()
    } else if (printerType === 'serial') {
      loadSerialPorts()
    }
  }, [printerType])

  const loadUsbDevices = async () => {
    const result = await window.electronAPI.printer.list('usb')
    if (result.success && result.printers) {
      setUsbDevices(result.printers)
    }
  }

  const loadSerialPorts = async () => {
    const result = await window.electronAPI.printer.list('serial')
    if (result.success && result.printers) {
      setSerialPorts(result.printers)
    }
  }

  const handleConfigure = async () => {
    let config: any = {
      type: printerType,
      width: parseInt(printerWidth),
    }

    if (printerType === 'network') {
      config.endpoint = `${networkIp}:${networkPort}`
    } else if (printerType === 'usb' && selectedUsb) {
      config.vendorId = selectedUsb.vendorId
      config.productId = selectedUsb.productId
    } else if (printerType === 'serial' && selectedSerial) {
      config.endpoint = selectedSerial
    } else {
      setStatus('⚠️ Seleziona un dispositivo')
      return
    }

    const result = await window.electronAPI.printer.configure(config)
    if (result.success) {
      setStatus('✅ Stampante configurata!')
    } else {
      setStatus(`❌ Errore: ${result.error}`)
    }
  }

  const handleTest = async () => {
    setTesting(true)
    setStatus('📄 Stampa di test in corso...')

    const result = await window.electronAPI.printer.test()

    if (result.success) {
      setStatus('✅ Test completato! Controlla la stampante.')
    } else {
      setStatus(`❌ Errore test: ${result.error}`)
    }

    setTesting(false)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Impostazioni Stampante</h2>
        <p className="text-muted-foreground">
          Configura la connessione alla tua stampante termica
        </p>
      </div>

      {/* Tipo stampante */}
      <Card>
        <CardHeader>
          <CardTitle>Tipo di Connessione</CardTitle>
          <CardDescription>Seleziona come si connette la stampante</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <Button
              variant={printerType === 'network' ? 'default' : 'outline'}
              onClick={() => setPrinterType('network')}
              className="h-24 flex flex-col gap-2"
            >
              <Wifi className="w-8 h-8" />
              <span>Network</span>
              <span className="text-xs opacity-70">WiFi/Ethernet</span>
            </Button>

            <Button
              variant={printerType === 'usb' ? 'default' : 'outline'}
              onClick={() => setPrinterType('usb')}
              className="h-24 flex flex-col gap-2"
            >
              <Usb className="w-8 h-8" />
              <span>USB</span>
              <span className="text-xs opacity-70">Connessione diretta</span>
            </Button>

            <Button
              variant={printerType === 'serial' ? 'default' : 'outline'}
              onClick={() => setPrinterType('serial')}
              className="h-24 flex flex-col gap-2"
            >
              <Cable className="w-8 h-8" />
              <span>Seriale</span>
              <span className="text-xs opacity-70">COM/ttyUSB</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Configurazione Network */}
      {printerType === 'network' && (
        <Card>
          <CardHeader>
            <CardTitle>Configurazione Network</CardTitle>
            <CardDescription>Inserisci l'indirizzo IP della stampante</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="ip">Indirizzo IP</Label>
                <Input
                  id="ip"
                  value={networkIp}
                  onChange={(e) => setNetworkIp(e.target.value)}
                  placeholder="192.168.1.100"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="port">Porta</Label>
                <Input
                  id="port"
                  value={networkPort}
                  onChange={(e) => setNetworkPort(e.target.value)}
                  placeholder="9100"
                />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Configurazione USB */}
      {printerType === 'usb' && (
        <Card>
          <CardHeader>
            <CardTitle>Dispositivi USB</CardTitle>
            <CardDescription>Seleziona la stampante dalla lista</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button onClick={loadUsbDevices} variant="outline" size="sm">
              Aggiorna Lista
            </Button>
            <div className="space-y-2">
              {usbDevices.length === 0 ? (
                <p className="text-sm text-muted-foreground">Nessun dispositivo trovato</p>
              ) : (
                usbDevices.map((device, index) => (
                  <Button
                    key={index}
                    variant={
                      selectedUsb?.vendorId === device.vendorId &&
                      selectedUsb?.productId === device.productId
                        ? 'default'
                        : 'outline'
                    }
                    onClick={() =>
                      setSelectedUsb({ vendorId: device.vendorId, productId: device.productId })
                    }
                    className="w-full justify-start"
                  >
                    <Usb className="w-4 h-4 mr-2" />
                    {device.name}
                  </Button>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Configurazione Seriale */}
      {printerType === 'serial' && (
        <Card>
          <CardHeader>
            <CardTitle>Porte Seriali</CardTitle>
            <CardDescription>Seleziona la porta COM/ttyUSB</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button onClick={loadSerialPorts} variant="outline" size="sm">
              Aggiorna Lista
            </Button>
            <div className="space-y-2">
              {serialPorts.length === 0 ? (
                <p className="text-sm text-muted-foreground">Nessuna porta trovata</p>
              ) : (
                serialPorts.map((port, index) => (
                  <Button
                    key={index}
                    variant={selectedSerial === port.path ? 'default' : 'outline'}
                    onClick={() => setSelectedSerial(port.path)}
                    className="w-full justify-start"
                  >
                    <Cable className="w-4 h-4 mr-2" />
                    {port.path} {port.manufacturer && `(${port.manufacturer})`}
                  </Button>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Larghezza stampante */}
      <Card>
        <CardHeader>
          <CardTitle>Larghezza Carta</CardTitle>
          <CardDescription>Scegli la larghezza della tua stampante</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Button
              variant={printerWidth === '384' ? 'default' : 'outline'}
              onClick={() => setPrinterWidth('384')}
            >
              58mm (384px)
            </Button>
            <Button
              variant={printerWidth === '576' ? 'default' : 'outline'}
              onClick={() => setPrinterWidth('576')}
            >
              80mm (576px)
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Azioni */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <Button onClick={handleConfigure} className="flex-1" size="lg">
              <CheckCircle2 className="w-4 h-4 mr-2" />
              Salva Configurazione
            </Button>
            <Button onClick={handleTest} variant="outline" size="lg" disabled={testing}>
              <Printer className="w-4 h-4 mr-2" />
              Test Stampa
            </Button>
          </div>
          {status && (
            <p className="mt-4 text-sm text-center font-medium">{status}</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
