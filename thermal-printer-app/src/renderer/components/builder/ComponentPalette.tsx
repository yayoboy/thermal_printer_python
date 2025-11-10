import { useDraggable } from '@dnd-kit/core'
import { Type, Heading1, Table, Minus, Image, Barcode } from 'lucide-react'
import { Card } from '../ui/card'
import { ComponentType } from '../TemplateBuilder'

interface DraggableComponentProps {
  id: ComponentType
  icon: React.ReactNode
  label: string
  description: string
}

function DraggableComponent({ id, icon, label, description }: DraggableComponentProps) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id,
  })

  const style = transform
    ? {
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
        opacity: isDragging ? 0.5 : 1,
      }
    : undefined

  return (
    <Card
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className="p-3 cursor-grab active:cursor-grabbing hover:bg-accent transition-colors"
    >
      <div className="flex items-start gap-3">
        <div className="p-2 rounded-md bg-primary/10 text-primary">
          {icon}
        </div>
        <div className="flex-1 min-w-0">
          <div className="font-medium text-sm">{label}</div>
          <div className="text-xs text-muted-foreground">{description}</div>
        </div>
      </div>
    </Card>
  )
}

export function ComponentPalette() {
  const components: DraggableComponentProps[] = [
    {
      id: 'heading',
      icon: <Heading1 className="w-4 h-4" />,
      label: 'Titolo',
      description: 'Testo grande e in grassetto',
    },
    {
      id: 'text',
      icon: <Type className="w-4 h-4" />,
      label: 'Testo',
      description: 'Paragrafo di testo normale',
    },
    {
      id: 'table',
      icon: <Table className="w-4 h-4" />,
      label: 'Tabella',
      description: 'Tabella per dati strutturati',
    },
    {
      id: 'separator',
      icon: <Minus className="w-4 h-4" />,
      label: 'Separatore',
      description: 'Linea orizzontale',
    },
    {
      id: 'barcode',
      icon: <Barcode className="w-4 h-4" />,
      label: 'Barcode',
      description: 'Codice a barre simulato',
    },
  ]

  return (
    <div className="space-y-2">
      {components.map((comp) => (
        <DraggableComponent key={comp.id} {...comp} />
      ))}
    </div>
  )
}
