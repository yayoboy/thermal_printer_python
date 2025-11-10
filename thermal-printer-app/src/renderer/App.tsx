import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import { TemplateBuilder } from './components/TemplateBuilder'
import { PrinterSettings } from './components/PrinterSettings'
import { TemplateManager } from './components/TemplateManager'
import { Printer, FileCode, Settings } from 'lucide-react'

function App() {
  const [activeTab, setActiveTab] = useState('builder')

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Printer className="w-6 h-6" />
              <h1 className="text-xl font-bold">Thermal Printer</h1>
            </div>
            <p className="text-sm text-muted-foreground">
              Drag & Drop Builder per Stampanti Termiche
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full flex flex-col">
          <div className="border-b bg-muted/40">
            <div className="container mx-auto px-4">
              <TabsList className="h-12">
                <TabsTrigger value="builder" className="gap-2">
                  <FileCode className="w-4 h-4" />
                  Template Builder
                </TabsTrigger>
                <TabsTrigger value="templates" className="gap-2">
                  <FileCode className="w-4 h-4" />
                  Template Salvati
                </TabsTrigger>
                <TabsTrigger value="settings" className="gap-2">
                  <Settings className="w-4 h-4" />
                  Impostazioni Stampante
                </TabsTrigger>
              </TabsList>
            </div>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="builder" className="h-full m-0 p-0">
              <TemplateBuilder />
            </TabsContent>

            <TabsContent value="templates" className="h-full m-0">
              <div className="container mx-auto px-4 py-6">
                <TemplateManager />
              </div>
            </TabsContent>

            <TabsContent value="settings" className="h-full m-0">
              <div className="container mx-auto px-4 py-6">
                <PrinterSettings />
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </main>
    </div>
  )
}

export default App
