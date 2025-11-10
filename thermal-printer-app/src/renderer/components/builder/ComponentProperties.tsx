import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Button } from '../ui/button'
import { TemplateComponent, AVAILABLE_FONTS } from '../TemplateBuilder'
import { Select } from '../ui/select'
import * as Icons from 'lucide-react'
import { useState } from 'react'

interface ComponentPropertiesProps {
  component: TemplateComponent
  onUpdate: (props: any) => void
}

// Icone popolari Lucide
const POPULAR_ICONS = [
  'Heart', 'Star', 'Check', 'X', 'AlertCircle', 'Info', 'ShoppingCart',
  'User', 'Mail', 'Phone', 'Home', 'Settings', 'Search', 'Calendar',
  'Clock', 'MapPin', 'Gift', 'Truck', 'CreditCard', 'DollarSign'
]

export function ComponentProperties({ component, onUpdate }: ComponentPropertiesProps) {
  const [showIconPicker, setShowIconPicker] = useState(false)

  const updateProp = (key: string, value: any) => {
    onUpdate({ ...component.props, [key]: value })
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        const base64 = event.target?.result as string
        updateProp('src', base64)
      }
      reader.readAsDataURL(file)
    }
  }

  const renderProperties = () => {
    switch (component.type) {
      case 'text':
      case 'heading':
        return (
          <div className="space-y-4">
            <div>
              <Label>Contenuto</Label>
              <Input
                value={component.props.content}
                onChange={(e) => updateProp('content', e.target.value)}
              />
            </div>

            <div>
              <Label>Font</Label>
              <select
                value={component.props.fontFamily}
                onChange={(e) => updateProp('fontFamily', e.target.value)}
                className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                {AVAILABLE_FONTS.map((font) => (
                  <option key={font} value={font} style={{ fontFamily: font }}>
                    {font.split(',')[0]}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <Label>Dimensione Font</Label>
              <Input
                type="number"
                value={component.props.fontSize}
                onChange={(e) => updateProp('fontSize', parseInt(e.target.value))}
              />
            </div>

            <div>
              <Label>Colore</Label>
              <div className="flex gap-2">
                <Input
                  type="color"
                  value={component.props.color}
                  onChange={(e) => updateProp('color', e.target.value)}
                  className="w-20 h-10"
                />
                <Input
                  type="text"
                  value={component.props.color}
                  onChange={(e) => updateProp('color', e.target.value)}
                  placeholder="#000000"
                  className="flex-1"
                />
              </div>
            </div>

            <div>
              <Label>Allineamento</Label>
              <div className="grid grid-cols-3 gap-2 mt-2">
                <Button
                  variant={component.props.align === 'left' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'left')}
                >
                  Sinistra
                </Button>
                <Button
                  variant={component.props.align === 'center' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'center')}
                >
                  Centro
                </Button>
                <Button
                  variant={component.props.align === 'right' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'right')}
                >
                  Destra
                </Button>
              </div>
            </div>

            {component.type === 'heading' && (
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="bold"
                  checked={component.props.bold}
                  onChange={(e) => updateProp('bold', e.target.checked)}
                  className="rounded"
                />
                <Label htmlFor="bold">Grassetto</Label>
              </div>
            )}
          </div>
        )

      case 'icon':
        return (
          <div className="space-y-4">
            <div>
              <Label>Icona</Label>
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => setShowIconPicker(!showIconPicker)}
              >
                {React.createElement((Icons as any)[component.props.name] || Icons.Heart, { className: 'w-4 h-4 mr-2' })}
                {component.props.name}
              </Button>

              {showIconPicker && (
                <div className="mt-2 p-2 border rounded-lg max-h-64 overflow-y-auto grid grid-cols-4 gap-2">
                  {POPULAR_ICONS.map((iconName) => {
                    const Icon = (Icons as any)[iconName]
                    return (
                      <Button
                        key={iconName}
                        variant={component.props.name === iconName ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => {
                          updateProp('name', iconName)
                          setShowIconPicker(false)
                        }}
                        className="flex flex-col gap-1 h-auto py-2"
                      >
                        <Icon className="w-5 h-5" />
                        <span className="text-xs">{iconName}</span>
                      </Button>
                    )
                  })}
                </div>
              )}
            </div>

            <div>
              <Label>Dimensione</Label>
              <Input
                type="number"
                value={component.props.size}
                onChange={(e) => updateProp('size', parseInt(e.target.value))}
              />
            </div>

            <div>
              <Label>Colore</Label>
              <div className="flex gap-2">
                <Input
                  type="color"
                  value={component.props.color}
                  onChange={(e) => updateProp('color', e.target.value)}
                  className="w-20 h-10"
                />
                <Input
                  type="text"
                  value={component.props.color}
                  onChange={(e) => updateProp('color', e.target.value)}
                  placeholder="#000000"
                  className="flex-1"
                />
              </div>
            </div>

            <div>
              <Label>Allineamento</Label>
              <div className="grid grid-cols-3 gap-2 mt-2">
                <Button
                  variant={component.props.align === 'left' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'left')}
                >
                  Sinistra
                </Button>
                <Button
                  variant={component.props.align === 'center' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'center')}
                >
                  Centro
                </Button>
                <Button
                  variant={component.props.align === 'right' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'right')}
                >
                  Destra
                </Button>
              </div>
            </div>
          </div>
        )

      case 'image':
        return (
          <div className="space-y-4">
            <div>
              <Label>URL Immagine</Label>
              <Input
                value={component.props.src}
                onChange={(e) => updateProp('src', e.target.value)}
                placeholder="https://example.com/image.png"
              />
            </div>

            <div>
              <Label>Oppure Carica File</Label>
              <Input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="cursor-pointer"
              />
            </div>

            {component.props.src && (
              <div className="border rounded-lg p-2">
                <img
                  src={component.props.src}
                  alt={component.props.alt}
                  className="max-w-full h-auto max-h-32 mx-auto"
                />
              </div>
            )}

            <div>
              <Label>Testo Alternativo</Label>
              <Input
                value={component.props.alt}
                onChange={(e) => updateProp('alt', e.target.value)}
                placeholder="Descrizione immagine"
              />
            </div>

            <div>
              <Label>Larghezza Max (px)</Label>
              <Input
                type="number"
                value={component.props.width}
                onChange={(e) => updateProp('width', parseInt(e.target.value))}
              />
            </div>

            <div>
              <Label>Allineamento</Label>
              <div className="grid grid-cols-3 gap-2 mt-2">
                <Button
                  variant={component.props.align === 'left' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'left')}
                >
                  Sinistra
                </Button>
                <Button
                  variant={component.props.align === 'center' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'center')}
                >
                  Centro
                </Button>
                <Button
                  variant={component.props.align === 'right' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('align', 'right')}
                >
                  Destra
                </Button>
              </div>
            </div>
          </div>
        )

      case 'decorator':
        return (
          <div className="space-y-4">
            <div>
              <Label>Contenuto</Label>
              <Input
                value={component.props.content}
                onChange={(e) => updateProp('content', e.target.value)}
              />
            </div>

            <div>
              <Label>Padding (px)</Label>
              <Input
                type="number"
                value={component.props.padding}
                onChange={(e) => updateProp('padding', parseInt(e.target.value))}
              />
            </div>

            <div>
              <Label>Spessore Bordo (px)</Label>
              <Input
                type="number"
                value={component.props.borderWidth}
                onChange={(e) => updateProp('borderWidth', parseInt(e.target.value))}
              />
            </div>

            <div>
              <Label>Stile Bordo</Label>
              <select
                value={component.props.borderStyle}
                onChange={(e) => updateProp('borderStyle', e.target.value)}
                className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                <option value="solid">Solido</option>
                <option value="dashed">Tratteggiato</option>
                <option value="dotted">Punteggiato</option>
                <option value="double">Doppio</option>
              </select>
            </div>

            <div>
              <Label>Colore Bordo</Label>
              <div className="flex gap-2">
                <Input
                  type="color"
                  value={component.props.borderColor}
                  onChange={(e) => updateProp('borderColor', e.target.value)}
                  className="w-20 h-10"
                />
                <Input
                  type="text"
                  value={component.props.borderColor}
                  onChange={(e) => updateProp('borderColor', e.target.value)}
                  placeholder="#000000"
                  className="flex-1"
                />
              </div>
            </div>

            <div>
              <Label>Colore Sfondo</Label>
              <div className="flex gap-2">
                <Input
                  type="color"
                  value={component.props.backgroundColor}
                  onChange={(e) => updateProp('backgroundColor', e.target.value)}
                  className="w-20 h-10"
                />
                <Input
                  type="text"
                  value={component.props.backgroundColor}
                  onChange={(e) => updateProp('backgroundColor', e.target.value)}
                  placeholder="#ffffff"
                  className="flex-1"
                />
              </div>
            </div>

            <div>
              <Label>Raggio Bordo (px)</Label>
              <Input
                type="number"
                value={component.props.borderRadius}
                onChange={(e) => updateProp('borderRadius', parseInt(e.target.value))}
              />
            </div>
          </div>
        )

      case 'table':
        return (
          <div className="space-y-4">
            <div>
              <Label>Righe Tabella</Label>
              <div className="mt-2 space-y-2">
                {component.props.rows.map((row: string[], i: number) => (
                  <div key={i} className="space-y-1">
                    <Label className="text-xs">Riga {i + 1}</Label>
                    {row.map((cell: string, j: number) => (
                      <Input
                        key={j}
                        value={cell}
                        placeholder={`Colonna ${j + 1}`}
                        onChange={(e) => {
                          const newRows = [...component.props.rows]
                          newRows[i][j] = e.target.value
                          updateProp('rows', newRows)
                        }}
                        className="text-sm"
                      />
                    ))}
                  </div>
                ))}
              </div>
              <Button
                variant="outline"
                size="sm"
                className="w-full mt-2"
                onClick={() => {
                  const newRows = [
                    ...component.props.rows,
                    Array(component.props.rows[0].length).fill(''),
                  ]
                  updateProp('rows', newRows)
                }}
              >
                Aggiungi Riga
              </Button>
            </div>
          </div>
        )

      case 'separator':
        return (
          <div className="space-y-4">
            <div>
              <Label>Stile</Label>
              <div className="grid grid-cols-2 gap-2 mt-2">
                <Button
                  variant={component.props.style === 'solid' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('style', 'solid')}
                >
                  Solido
                </Button>
                <Button
                  variant={component.props.style === 'dashed' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => updateProp('style', 'dashed')}
                >
                  Tratteggiato
                </Button>
              </div>
            </div>

            <div>
              <Label>Spessore (px)</Label>
              <Input
                type="number"
                value={component.props.thickness}
                onChange={(e) => updateProp('thickness', parseInt(e.target.value))}
              />
            </div>

            <div>
              <Label>Colore</Label>
              <div className="flex gap-2">
                <Input
                  type="color"
                  value={component.props.color}
                  onChange={(e) => updateProp('color', e.target.value)}
                  className="w-20 h-10"
                />
                <Input
                  type="text"
                  value={component.props.color}
                  onChange={(e) => updateProp('color', e.target.value)}
                  placeholder="#000000"
                  className="flex-1"
                />
              </div>
            </div>
          </div>
        )

      case 'barcode':
        return (
          <div className="space-y-4">
            <div>
              <Label>Valore Barcode</Label>
              <Input
                value={component.props.value}
                onChange={(e) => updateProp('value', e.target.value)}
                placeholder="1234567890"
              />
            </div>
            <div className="text-xs text-muted-foreground">
              Nota: Questo è un barcode simulato. Per veri barcode, usa una libreria dedicata.
            </div>
          </div>
        )

      default:
        return <p className="text-sm text-muted-foreground">Nessuna proprietà disponibile</p>
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base capitalize">{component.type}</CardTitle>
      </CardHeader>
      <CardContent>{renderProperties()}</CardContent>
    </Card>
  )
}
