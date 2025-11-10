import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Button } from '../ui/button'
import { TemplateComponent } from '../TemplateBuilder'

interface ComponentPropertiesProps {
  component: TemplateComponent
  onUpdate: (props: any) => void
}

export function ComponentProperties({ component, onUpdate }: ComponentPropertiesProps) {
  const updateProp = (key: string, value: any) => {
    onUpdate({ ...component.props, [key]: value })
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
              <Label>Dimensione Font</Label>
              <Input
                type="number"
                value={component.props.fontSize}
                onChange={(e) => updateProp('fontSize', parseInt(e.target.value))}
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
