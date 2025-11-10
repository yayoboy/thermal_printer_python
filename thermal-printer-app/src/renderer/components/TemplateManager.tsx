import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { FileCode, Trash2, Download, Upload } from 'lucide-react'

export function TemplateManager() {
  const [templates, setTemplates] = useState<string[]>([])
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null)
  const [templateContent, setTemplateContent] = useState<string>('')

  useEffect(() => {
    loadTemplates()
  }, [])

  const loadTemplates = async () => {
    const result = await window.electronAPI.template.list()
    if (result.success && result.templates) {
      setTemplates(result.templates)
    }
  }

  const handleSelectTemplate = async (name: string) => {
    setSelectedTemplate(name)
    const result = await window.electronAPI.template.load(name)
    if (result.success && result.content) {
      setTemplateContent(result.content)
    }
  }

  const handleExport = () => {
    if (!templateContent) return

    const blob = new Blob([templateContent], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${selectedTemplate || 'template'}.html`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h2 className="text-3xl font-bold tracking-tight">Template Salvati</h2>
        <p className="text-muted-foreground">
          Gestisci i tuoi template per stampanti termiche
        </p>
      </div>

      <div className="grid grid-cols-12 gap-6">
        {/* Lista template */}
        <div className="col-span-4">
          <Card>
            <CardHeader>
              <CardTitle>I Tuoi Template</CardTitle>
              <CardDescription>
                {templates.length} template salvati
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {templates.length === 0 ? (
                  <p className="text-sm text-muted-foreground text-center py-8">
                    Nessun template salvato.<br />
                    Crea il tuo primo template nel Builder!
                  </p>
                ) : (
                  templates.map((name) => (
                    <Button
                      key={name}
                      variant={selectedTemplate === name ? 'default' : 'outline'}
                      onClick={() => handleSelectTemplate(name)}
                      className="w-full justify-start"
                    >
                      <FileCode className="w-4 h-4 mr-2" />
                      {name}
                    </Button>
                  ))
                )}
              </div>
              <Button
                onClick={loadTemplates}
                variant="outline"
                size="sm"
                className="w-full mt-4"
              >
                Aggiorna
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Preview template */}
        <div className="col-span-8">
          <Card className="h-full">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>
                    {selectedTemplate || 'Seleziona un template'}
                  </CardTitle>
                  <CardDescription>
                    Anteprima del codice HTML
                  </CardDescription>
                </div>
                {selectedTemplate && (
                  <div className="flex gap-2">
                    <Button
                      onClick={handleExport}
                      variant="outline"
                      size="sm"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Esporta
                    </Button>
                  </div>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {templateContent ? (
                <div className="space-y-4">
                  <div className="bg-muted rounded-lg p-4 font-mono text-sm overflow-auto max-h-96">
                    <pre>{templateContent}</pre>
                  </div>
                  <div className="border rounded-lg p-4">
                    <h4 className="font-semibold mb-2">Anteprima Rendering:</h4>
                    <div
                      className="border rounded bg-white p-2"
                      dangerouslySetInnerHTML={{ __html: templateContent }}
                    />
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-muted-foreground">
                  <FileCode className="w-16 h-16 mx-auto mb-4 opacity-20" />
                  <p>Seleziona un template per visualizzarlo</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
