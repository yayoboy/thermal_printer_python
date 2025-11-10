import { useState } from 'react'
import { DndContext, DragEndEvent, DragOverlay, DragStartEvent, closestCenter } from '@dnd-kit/core'
import { SortableContext, arrayMove, verticalListSortingStrategy } from '@dnd-kit/sortable'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { ComponentPalette } from './builder/ComponentPalette'
import { SortableComponent } from './builder/SortableComponent'
import { ComponentProperties } from './builder/ComponentProperties'
import { Printer, Save, Eye, Code } from 'lucide-react'

// Tipi di componenti
export type ComponentType = 'text' | 'heading' | 'table' | 'separator' | 'image' | 'barcode'

export interface TemplateComponent {
  id: string
  type: ComponentType
  props: any
}

export function TemplateBuilder() {
  const [components, setComponents] = useState<TemplateComponent[]>([])
  const [selectedComponent, setSelectedComponent] = useState<TemplateComponent | null>(null)
  const [activeId, setActiveId] = useState<string | null>(null)
  const [preview, setPreview] = useState<string>('')
  const [templateName, setTemplateName] = useState('')
  const [showCode, setShowCode] = useState(false)
  const [status, setStatus] = useState('')

  // Drag & Drop handlers
  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string)
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    setActiveId(null)

    if (!over) {
      // Aggiunto nuovo componente dalla palette
      const type = active.id as ComponentType
      addComponent(type)
      return
    }

    if (active.id !== over.id) {
      setComponents((items) => {
        const oldIndex = items.findIndex((item) => item.id === active.id)
        const newIndex = items.findIndex((item) => item.id === over.id)
        return arrayMove(items, oldIndex, newIndex)
      })
    }
  }

  const addComponent = (type: ComponentType) => {
    const newComponent: TemplateComponent = {
      id: `${type}-${Date.now()}`,
      type,
      props: getDefaultProps(type),
    }
    setComponents([...components, newComponent])
  }

  const getDefaultProps = (type: ComponentType) => {
    switch (type) {
      case 'text':
        return { content: 'Testo di esempio', align: 'left', fontSize: 12 }
      case 'heading':
        return { content: 'Titolo', align: 'center', fontSize: 18, bold: true }
      case 'table':
        return {
          rows: [
            ['Prodotto', 'Prezzo'],
            ['Articolo 1', '€ 10.00'],
          ],
        }
      case 'separator':
        return { style: 'dashed' }
      case 'image':
        return { src: '', alt: 'Immagine', width: 200 }
      case 'barcode':
        return { value: '1234567890', type: 'code128' }
      default:
        return {}
    }
  }

  const updateComponent = (id: string, props: any) => {
    setComponents(
      components.map((comp) => (comp.id === id ? { ...comp, props } : comp))
    )
  }

  const deleteComponent = (id: string) => {
    setComponents(components.filter((comp) => comp.id !== id))
    if (selectedComponent?.id === id) {
      setSelectedComponent(null)
    }
  }

  const generateHTML = () => {
    let html = '<div style="font-family: Arial, sans-serif; padding: 10px;">\n'

    components.forEach((comp) => {
      switch (comp.type) {
        case 'text':
          html += `  <p style="text-align: ${comp.props.align}; font-size: ${comp.props.fontSize}px; margin: 8px 0;">${comp.props.content}</p>\n`
          break
        case 'heading':
          html += `  <h1 style="text-align: ${comp.props.align}; font-size: ${comp.props.fontSize}px; font-weight: ${comp.props.bold ? 'bold' : 'normal'}; margin: 10px 0;">${comp.props.content}</h1>\n`
          break
        case 'table':
          html += '  <table style="width: 100%; border-collapse: collapse; margin: 10px 0;">\n'
          comp.props.rows.forEach((row: string[], i: number) => {
            html += '    <tr>\n'
            row.forEach((cell: string) => {
              html += `      <${i === 0 ? 'th' : 'td'} style="padding: 4px; text-align: left; ${i === 0 ? 'font-weight: bold;' : ''}">${cell}</${i === 0 ? 'th' : 'td'}>\n`
            })
            html += '    </tr>\n'
          })
          html += '  </table>\n'
          break
        case 'separator':
          html += `  <hr style="border: none; border-top: 1px ${comp.props.style} #000; margin: 10px 0;" />\n`
          break
        case 'barcode':
          html += `  <div style="text-align: center; font-family: monospace; letter-spacing: 2px; margin: 10px 0;">${comp.props.value}</div>\n`
          break
      }
    })

    html += '</div>'
    return html
  }

  const handlePreview = async () => {
    const html = generateHTML()
    setPreview(html)
  }

  const handleSave = async () => {
    if (!templateName) {
      setStatus('⚠️ Inserisci un nome per il template')
      return
    }

    const html = generateHTML()
    const result = await window.electronAPI.template.save(templateName, html)

    if (result.success) {
      setStatus('✅ Template salvato!')
    } else {
      setStatus(`❌ Errore: ${result.error}`)
    }
  }

  const handlePrint = async () => {
    const html = generateHTML()
    setStatus('🖨️ Stampa in corso...')

    const result = await window.electronAPI.printer.printHtml(html, 384)

    if (result.success) {
      setStatus('✅ Stampato!')
    } else {
      setStatus(`❌ Errore: ${result.error}`)
    }
  }

  return (
    <div className="h-full flex">
      {/* Pannello sinistro - Palette componenti */}
      <div className="w-64 border-r bg-muted/40 p-4 overflow-y-auto">
        <h3 className="font-semibold mb-4">Componenti</h3>
        <ComponentPalette />
      </div>

      {/* Area centrale - Canvas */}
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-2xl mx-auto space-y-6">
          {/* Header */}
          <Card>
            <CardHeader>
              <CardTitle>Template Builder</CardTitle>
              <CardDescription>
                Trascina componenti per creare il tuo template
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <Input
                  placeholder="Nome template..."
                  value={templateName}
                  onChange={(e) => setTemplateName(e.target.value)}
                />
                <Button onClick={handleSave} variant="outline">
                  <Save className="w-4 h-4 mr-2" />
                  Salva
                </Button>
                <Button onClick={handlePreview} variant="outline">
                  <Eye className="w-4 h-4 mr-2" />
                  Preview
                </Button>
                <Button onClick={() => setShowCode(!showCode)} variant="outline">
                  <Code className="w-4 h-4 mr-2" />
                  HTML
                </Button>
                <Button onClick={handlePrint}>
                  <Printer className="w-4 h-4 mr-2" />
                  Stampa
                </Button>
              </div>
              {status && <p className="mt-2 text-sm font-medium">{status}</p>}
            </CardContent>
          </Card>

          {/* Canvas - Drop zone */}
          <Card>
            <CardHeader>
              <CardTitle>Canvas</CardTitle>
            </CardHeader>
            <CardContent>
              <DndContext
                collisionDetection={closestCenter}
                onDragStart={handleDragStart}
                onDragEnd={handleDragEnd}
              >
                <div className="min-h-96 border-2 border-dashed rounded-lg p-4 bg-white">
                  {components.length === 0 ? (
                    <div className="h-64 flex items-center justify-center text-muted-foreground">
                      Trascina qui i componenti dalla palette
                    </div>
                  ) : (
                    <SortableContext
                      items={components.map((c) => c.id)}
                      strategy={verticalListSortingStrategy}
                    >
                      {components.map((component) => (
                        <SortableComponent
                          key={component.id}
                          component={component}
                          onSelect={() => setSelectedComponent(component)}
                          onDelete={() => deleteComponent(component.id)}
                          isSelected={selectedComponent?.id === component.id}
                        />
                      ))}
                    </SortableContext>
                  )}
                </div>
              </DndContext>
            </CardContent>
          </Card>

          {/* Preview HTML */}
          {showCode && (
            <Card>
              <CardHeader>
                <CardTitle>Codice HTML</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-xs">
                  {generateHTML()}
                </pre>
              </CardContent>
            </Card>
          )}

          {/* Preview rendering */}
          {preview && (
            <Card>
              <CardHeader>
                <CardTitle>Anteprima</CardTitle>
              </CardHeader>
              <CardContent>
                <div
                  className="border rounded-lg p-4 bg-white"
                  dangerouslySetInnerHTML={{ __html: preview }}
                />
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Pannello destro - Proprietà */}
      <div className="w-80 border-l bg-muted/40 p-4 overflow-y-auto">
        <h3 className="font-semibold mb-4">Proprietà</h3>
        {selectedComponent ? (
          <ComponentProperties
            component={selectedComponent}
            onUpdate={(props) => updateComponent(selectedComponent.id, props)}
          />
        ) : (
          <p className="text-sm text-muted-foreground">
            Seleziona un componente per modificarne le proprietà
          </p>
        )}
      </div>
    </div>
  )
}
