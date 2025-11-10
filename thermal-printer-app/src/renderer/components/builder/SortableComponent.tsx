import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { Card } from '../ui/card'
import { Button } from '../ui/button'
import { GripVertical, Trash2 } from 'lucide-react'
import { TemplateComponent } from '../TemplateBuilder'
import * as Icons from 'lucide-react'

interface SortableComponentProps {
  component: TemplateComponent
  onSelect: () => void
  onDelete: () => void
  isSelected: boolean
}

export function SortableComponent({
  component,
  onSelect,
  onDelete,
  isSelected,
}: SortableComponentProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: component.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  }

  const renderComponent = () => {
    switch (component.type) {
      case 'text': {
        const textStyle: React.CSSProperties = {
          textAlign: component.props.align,
          fontSize: component.props.fontSize,
          fontFamily: component.props.fontFamily,
          fontWeight: component.props.fontWeight || '400',
        }

        if (component.props.useGradient) {
          textStyle.background = `linear-gradient(${component.props.gradientDirection}, ${component.props.gradientStart}, ${component.props.gradientEnd})`
          textStyle.WebkitBackgroundClip = 'text'
          textStyle.WebkitTextFillColor = 'transparent'
          textStyle.backgroundClip = 'text'
        } else {
          textStyle.color = component.props.color
        }

        return (
          <p style={textStyle}>
            {component.props.content}
          </p>
        )
      }
      case 'heading': {
        const headingStyle: React.CSSProperties = {
          textAlign: component.props.align,
          fontSize: component.props.fontSize,
          fontFamily: component.props.fontFamily,
          fontWeight: component.props.fontWeight || '700',
        }

        if (component.props.useGradient) {
          headingStyle.background = `linear-gradient(${component.props.gradientDirection}, ${component.props.gradientStart}, ${component.props.gradientEnd})`
          headingStyle.WebkitBackgroundClip = 'text'
          headingStyle.WebkitTextFillColor = 'transparent'
          headingStyle.backgroundClip = 'text'
        } else {
          headingStyle.color = component.props.color
        }

        return (
          <h1 style={headingStyle}>
            {component.props.content}
          </h1>
        )
      }
      case 'icon':
        const IconComponent = (Icons as any)[component.props.name] || Icons.Heart
        return (
          <div style={{ textAlign: component.props.align }}>
            <IconComponent
              size={component.props.size}
              color={component.props.color}
              style={{ display: 'inline-block' }}
            />
          </div>
        )
      case 'image':
        if (!component.props.src) {
          return (
            <div className="text-center text-muted-foreground text-sm border-2 border-dashed rounded p-4">
              Nessuna immagine caricata
            </div>
          )
        }
        return (
          <div style={{ textAlign: component.props.align }}>
            <img
              src={component.props.src}
              alt={component.props.alt}
              style={{ maxWidth: `${component.props.width}px`, height: 'auto' }}
            />
          </div>
        )
      case 'decorator': {
        const decoratorStyle: React.CSSProperties = {
          padding: `${component.props.padding}px`,
          border: `${component.props.borderWidth}px ${component.props.borderStyle} ${component.props.borderColor}`,
          borderRadius: `${component.props.borderRadius}px`,
        }

        if (component.props.useGradient) {
          decoratorStyle.background = `linear-gradient(${component.props.gradientDirection}, ${component.props.gradientStart}, ${component.props.gradientEnd})`
        } else {
          decoratorStyle.backgroundColor = component.props.backgroundColor
        }

        return (
          <div style={decoratorStyle}>
            {component.props.content}
          </div>
        )
      }
      case 'table':
        return (
          <table className="w-full border-collapse">
            <tbody>
              {component.props.rows.map((row: string[], i: number) => (
                <tr key={i}>
                  {row.map((cell: string, j: number) => (
                    <td
                      key={j}
                      className={`p-1 text-left ${i === 0 ? 'font-bold' : ''}`}
                    >
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )
      case 'separator':
        return (
          <hr
            style={{
              border: 'none',
              borderTop: `${component.props.thickness}px ${component.props.style} ${component.props.color}`,
            }}
          />
        )
      case 'barcode':
        return (
          <div className="text-center font-mono tracking-wider">
            {component.props.value}
          </div>
        )
      default:
        return null
    }
  }

  return (
    <Card
      ref={setNodeRef}
      style={style}
      className={`mb-2 p-3 ${isSelected ? 'ring-2 ring-primary' : ''}`}
      onClick={onSelect}
    >
      <div className="flex items-start gap-2">
        <div
          {...attributes}
          {...listeners}
          className="cursor-grab active:cursor-grabbing p-1 hover:bg-accent rounded"
        >
          <GripVertical className="w-4 h-4 text-muted-foreground" />
        </div>
        <div className="flex-1 min-w-0">{renderComponent()}</div>
        <Button
          variant="ghost"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onDelete()
          }}
          className="h-8 w-8 p-0"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>
    </Card>
  )
}
