import { useState } from 'react'
import { collectApi } from '@/services/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { useQuery } from '@tanstack/react-query'
import { RefreshCw, Plus, TestTube, Play } from 'lucide-react'

const mockConnectors = [
  {
    id: 'syslog',
    name: 'Syslog Collector',
    type: 'syslog',
    status: 'running',
    description: 'Receive logs via UDP/TCP syslog',
  },
  {
    id: 'http',
    name: 'HTTP Event Collector',
    type: 'http',
    status: 'running',
    description: 'REST API for log ingestion',
  },
  {
    id: 'kafka',
    name: 'Kafka Consumer',
    type: 'kafka',
    status: 'running',
    description: 'Consume events from Kafka topics',
  },
  {
    id: 'aws',
    name: 'AWS CloudTrail',
    type: 'cloud',
    status: 'configured',
    description: 'AWS audit logs and events',
  },
  {
    id: 'azure',
    name: 'Azure Activity Log',
    type: 'cloud',
    status: 'configured',
    description: 'Microsoft Azure activity logs',
  },
  {
    id: 'crowdstrike',
    name: 'CrowdStrike EDR',
    type: 'edr',
    status: 'stopped',
    description: 'Endpoint detection and response',
  },
]

export default function Settings() {
  const [testLoading, setTestLoading] = useState<string | null>(null)

  const { data: connectors, refetch } = useQuery({
    queryKey: ['connectors'],
    queryFn: () => collectApi.listConnectors(),
    initialData: { data: mockConnectors },
  })

  const handleTest = async (connectorId: string) => {
    setTestLoading(connectorId)
    try {
      await collectApi.testConnector(connectorId)
    } catch (err) {
      console.error(err)
    } finally {
      setTestLoading(null)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'configured':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
      case 'stopped':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-muted-foreground">
          Configure data sources and integrations
        </p>
      </div>

      {/* Connectors */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Data Connectors</CardTitle>
              <CardDescription>
                Configure and manage data collection sources
              </CardDescription>
            </div>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Connector
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            {connectors.data.map((connector: any) => (
              <div
                key={connector.id}
                className="p-4 border rounded-lg hover:bg-accent transition-colors"
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="font-semibold">{connector.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      {connector.description}
                    </p>
                  </div>
                  <Badge className={getStatusColor(connector.status)}>
                    {connector.status}
                  </Badge>
                </div>
                <div className="flex items-center justify-between mt-4">
                  <span className="text-xs text-muted-foreground uppercase">
                    {connector.type}
                  </span>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleTest(connector.id)}
                      disabled={testLoading === connector.id}
                    >
                      <TestTube className="h-3 w-3 mr-1" />
                      Test
                    </Button>
                    <Button variant="outline" size="sm">
                      Configure
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Users */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Users</CardTitle>
              <CardDescription>
                Manage user access and roles
              </CardDescription>
            </div>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add User
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                  <span className="text-sm font-medium">A</span>
                </div>
                <div>
                  <p className="font-medium">admin</p>
                  <p className="text-sm text-muted-foreground">admin@siem.local</p>
                </div>
              </div>
              <Badge variant="secondary">admin</Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* API Keys */}
      <Card>
        <CardHeader>
          <CardTitle>API Keys</CardTitle>
          <CardDescription>
            Manage API keys for external integrations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div>
                <p className="font-medium">Default API Key</p>
                <p className="text-sm text-muted-foreground font-mono">
                  sk_live_••••••••••••••••••
                </p>
              </div>
              <Button variant="outline" size="sm">
                Regenerate
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* About */}
      <Card>
        <CardHeader>
          <CardTitle>About</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm">
            <p><strong>SIEM Platform</strong> v1.0.0</p>
            <p className="text-muted-foreground">
              Built with FastAPI, React, OpenSearch, and PostgreSQL
            </p>
            <p className="text-muted-foreground">
              Inspired by Stellar Cyber Open XDR
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
