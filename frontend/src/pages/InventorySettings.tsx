import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Bot, Key, Code, Webhook, Save, TestTube, 
  ChevronDown, ChevronRight, Copy, Check 
} from 'lucide-react'

// AI Providers configuration
const AI_PROVIDERS = [
  {
    id: 'openai',
    name: 'OpenAI',
    models: ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
    api_url: 'https://api.openai.com/v1/chat/completions',
    description: 'GPT-4 powered analysis'
  },
  {
    id: 'anthropic',
    name: 'Anthropic Claude',
    models: ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'],
    api_url: 'https://api.anthropic.com/v1/complete',
    description: 'Claude AI analysis'
  },
  {
    id: 'groq',
    name: 'Groq',
    models: ['llama2-70b-4096', 'mixtral-8x7b-32768', 'gemma-7b-it'],
    api_url: 'https://api.groq.com/openai/v1/chat/completions',
    description: 'Fast inference with Llama models'
  },
  {
    id: 'deepseek',
    name: 'DeepSeek',
    models: ['deepseek-chat'],
    api_url: 'https://api.deepseek.com/chat/completions',
    description: 'DeepSeek Coder/Chat models'
  },
  {
    id: 'ollama',
    name: 'Ollama (Local)',
    models: ['llama2', 'codellama', 'mistral', 'neural-chat', 'starcoder'],
    api_url: 'http://localhost:11434/api/generate',
    description: 'Run models locally'
  }
]

// Default AI Prompt
const DEFAULT_PROMPT = `You are a cybersecurity expert analyzing equipment for inclusion in an inventory system.

## Equipment Data:
- Hostname: {hostname}
- IP Address: {ip_address}
- MAC Address: {mac_address}
- OS: {os} {os_version}
- Asset Type: {asset_type}
- Manufacturer: {manufacturer}
- Model: {model}
- Location: {location}
- Department: {department}

## Decision Criteria:
1. Is this a legitimate enterprise asset?
2. Does it have proper identification?
3. Are there security concerns?

## Output Format (JSON only):
{{"decision": "approved|rejected|pending", "comments": "...", "confidence": 0.0-1.0, "suggested_tags": ["tag1"]}}`

export default function InventorySettingsPage() {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState('ai')
  const [copied, setCopied] = useState(false)
  
  // AI Configuration state
  const [aiConfig, setAiConfig] = useState({
    provider: 'openai',
    model: 'gpt-4',
    apiUrl: 'https://api.openai.com/v1/chat/completions',
    apiKey: '',
    temperature: 0.3,
    maxTokens: 1000,
    promptTemplate: DEFAULT_PROMPT,
    isEnabled: true,
    autoProcess: true,
    webhookUrl: ''
  })
  
  const copyWebhookUrl = () => {
    navigator.clipboard.writeText('/api/v1/inventory/webhook/n8n')
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const testConnection = async () => {
    // TODO: Test AI connection
    alert('Test connection functionality - implement API call')
  }

  const saveConfig = async () => {
    // TODO: Save configuration to API
    alert('Configuration saved!')
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Inventory AI Configuration</h1>
          <p className="text-muted-foreground">
            Configure AI-powered inventory processing
          </p>
        </div>
        <Button onClick={saveConfig}>
          <Save className="h-4 w-4 mr-2" />
          Save Configuration
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="ai" className="flex items-center gap-2">
            <Bot className="h-4 w-4" />
            AI Provider
          </TabsTrigger>
          <TabsTrigger value="prompt" className="flex items-center gap-2">
            <Code className="h-4 w-4" />
            Prompt
          </TabsTrigger>
          <TabsTrigger value="webhook" className="flex items-center gap-2">
            <Webhook className="h-4 w-4" />
            N8N Webhook
          </TabsTrigger>
          <TabsTrigger value="rules" className="flex items-center gap-2">
            <Key className="h-4 w-4" />
            Rules
          </TabsTrigger>
        </TabsList>

        {/* AI Provider Tab */}
        <TabsContent value="ai" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>AI Provider Configuration</CardTitle>
              <CardDescription>
                Choose and configure your AI provider for inventory analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Provider Selection */}
              <div className="grid gap-4 md:grid-cols-5">
                {AI_PROVIDERS.map((provider) => (
                  <div
                    key={provider.id}
                    className={`p-4 border rounded-lg cursor-pointer transition-all ${
                      aiConfig.provider === provider.id
                        ? 'border-primary bg-primary/5'
                        : 'hover:border-gray-400'
                    }`}
                    onClick={() => setAiConfig({
                      ...aiConfig,
                      provider: provider.id,
                      apiUrl: provider.api_url
                    })}
                  >
                    <div className="font-medium">{provider.name}</div>
                    <div className="text-xs text-muted-foreground mt-1">
                      {provider.description}
                    </div>
                  </div>
                ))}
              </div>

              {/* Provider Details */}
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Model</label>
                  <select
                    value={aiConfig.model}
                    onChange={(e) => setAiConfig({ ...aiConfig, model: e.target.value })}
                    className="w-full h-10 px-3 border rounded-md bg-background"
                  >
                    {AI_PROVIDERS.find(p => p.id === aiConfig.provider)?.models.map(model => (
                      <option key={model} value={model}>{model}</option>
                    ))}
                  </select>
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Temperature</label>
                  <div className="flex items-center gap-4">
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={aiConfig.temperature}
                      onChange={(e) => setAiConfig({ ...aiConfig, temperature: parseFloat(e.target.value) })}
                      className="flex-1"
                    />
                    <span className="text-sm w-12">{aiConfig.temperature}</span>
                  </div>
                </div>
                
                <div className="space-y-2 md:col-span-2">
                  <label className="text-sm font-medium">API URL</label>
                  <Input
                    value={aiConfig.apiUrl}
                    onChange={(e) => setAiConfig({ ...aiConfig, apiUrl: e.target.value })}
                    placeholder="https://api..."
                  />
                </div>
                
                <div className="space-y-2 md:col-span-2">
                  <label className="text-sm font-medium">
                    API Key
                    <Badge variant="outline" className="ml-2">Encrypted</Badge>
                  </label>
                  <Input
                    type="password"
                    value={aiConfig.apiKey}
                    onChange={(e) => setAiConfig({ ...aiConfig, apiKey: e.target.value })}
                    placeholder="sk-..."
                  />
                </div>
              </div>

              {/* Options */}
              <div className="flex items-center gap-6 pt-4 border-t">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={aiConfig.isEnabled}
                    onChange={(e) => setAiConfig({ ...aiConfig, isEnabled: e.target.checked })}
                    className="rounded"
                  />
                  <span className="text-sm">Enable AI Processing</span>
                </label>
                
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={aiConfig.autoProcess}
                    onChange={(e) => setAiConfig({ ...aiConfig, autoProcess: e.target.checked })}
                    className="rounded"
                  />
                  <span className="text-sm">Auto-process incoming items</span>
                </label>
                
                <Button variant="outline" size="sm" onClick={testConnection}>
                  <TestTube className="h-4 w-4 mr-2" />
                  Test Connection
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Prompt Tab */}
        <TabsContent value="prompt" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>AI Prompt Template</CardTitle>
              <CardDescription>
                Customize how AI analyzes equipment data
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 bg-muted rounded-lg">
                <h4 className="font-medium mb-2">Available Variables</h4>
                <div className="flex flex-wrap gap-2">
                  {['{hostname}', '{ip_address}', '{mac_address}', '{os}', '{os_version}', '{asset_type}', '{manufacturer}', '{model}', '{serial_number}', '{location}', '{department}', '{owner}', '{tags}'].map(v => (
                    <code key={v} className="text-xs bg-background px-2 py-1 rounded">{v}</code>
                  ))}
                </div>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium">Prompt Template</label>
                <textarea
                  value={aiConfig.promptTemplate}
                  onChange={(e) => setAiConfig({ ...aiConfig, promptTemplate: e.target.value })}
                  className="w-full h-96 font-mono text-sm p-4 border rounded-md bg-background"
                  placeholder="Enter your prompt template..."
                />
              </div>
              
              <div className="flex justify-between">
                <Button variant="outline" onClick={() => setAiConfig({ ...aiConfig, promptTemplate: DEFAULT_PROMPT })}>
                  Reset to Default
                </Button>
                <Button variant="outline" onClick={testConnection}>
                  <TestTube className="h-4 w-4 mr-2" />
                  Test Prompt
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Webhook Tab */}
        <TabsContent value="webhook" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>N8N Integration</CardTitle>
              <CardDescription>
                Configure N8N to send equipment data to this endpoint
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="p-4 border rounded-lg bg-muted/50">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium">Webhook URL</h4>
                  <Button variant="ghost" size="sm" onClick={copyWebhookUrl}>
                    {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                  </Button>
                </div>
                <code className="text-sm block bg-background p-3 rounded">
                  POST {window.location.origin}/api/v1/inventory/webhook/n8n
                </code>
              </div>
              
              <div>
                <h4 className="font-medium mb-2">Expected JSON Format</h4>
                <pre className="text-sm bg-muted p-4 rounded-lg overflow-auto">
{`": [
    {
      "hostname": "web-server-{
  "items01",
      "ip_address": "10.0.0.10",
      "mac_address": "00:11:22:33:44:55",
      "os": "Ubuntu",
      "os_version": "22.04",
      "asset_type": "server",
      "manufacturer": "Dell",
      "model": "PowerEdge R740",
      "location": "Data Center A",
      "department": "IT",
      "owner": "admin@company.com",
      "tags": ["production", "web"],
      "source": "n8n_scan"
    }
  ]
}`}
                </pre>
              </div>
              
              <div className="grid gap-4 md:grid-cols-2">
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium mb-2">Required Fields</h4>
                  <ul className="text-sm space-y-1 text-muted-foreground">
                    <li>• hostname (optional)</li>
                    <li>• ip_address (optional)</li>
                    <li>• os (optional)</li>
                    <li>• source (optional, default: "n8n")</li>
                  </ul>
                </div>
                
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium mb-2">Optional Fields</h4>
                  <ul className="text-sm space-y-1 text-muted-foreground">
                    <li>• mac_address</li>
                    <li>• os_version</li>
                    <li>• asset_type</li>
                    <li>• manufacturer, model</li>
                    <li>• location, department, owner</li>
                    <li>• tags (array)</li>
                    <li>• metadata (object)</li>
                  </ul>
                </div>
              </div>
              
              <Button className="w-full" variant="outline">
                <Webhook className="h-4 w-4 mr-2" />
                Send Test Payload
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Rules Tab */}
        <TabsContent value="rules" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Processing Rules</CardTitle>
                  <CardDescription>
                    Fallback rules when AI is unavailable or for simple decisions
                  </CardDescription>
                </div>
                <Button size="sm">
                  Add Rule
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="p-8 text-center border rounded-lg text-muted-foreground">
                <Key className="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p>No processing rules configured</p>
                <p className="text-sm">Add rules to automatically approve/reject items based on conditions</p>
              </div>
              
              <div className="mt-4">
                <h4 className="font-medium mb-2">Example Rules</h4>
                <div className="space-y-2">
                  <div className="p-3 border rounded-lg">
                    <div className="flex items-center justify-between">
                      <Badge variant="success">Approve</Badge>
                      <span className="text-sm">If OS contains "Windows"</span>
                    </div>
                  </div>
                  <div className="p-3 border rounded-lg">
                    <div className="flex items-center justify-between">
                      <Badge variant="destructive">Reject</Badge>
                      <span className="text-sm">If hostname contains "test" AND department is "HR"</span>
                    </div>
                  </div>
                  <div className="p-3 border rounded-lg">
                    <div className="flex items-center justify-between">
                      <Badge variant="warning">Flag</Badge>
                      <span className="text-sm">If asset_type is "unknown"</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Processing Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Items Today
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              AI Approved
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-500">0</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              AI Rejected
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">0</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Pending Review
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-500">0</div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
