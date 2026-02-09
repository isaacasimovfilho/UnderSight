import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { alertsApi } from '@/services/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Filter, Search, RefreshCw } from 'lucide-react'

const mockAlerts = [
  {
    id: '1',
    title: 'Brute force attack detected',
    description: 'Multiple failed login attempts from external IP',
    severity: 'critical',
    status: 'new',
    source_type: 'firewall',
    risk_score: 85,
    created_at: '2026-02-09T05:00:00Z',
  },
  {
    id: '2',
    title: 'Suspicious PowerShell execution',
    description: 'Encoded PowerShell command detected on endpoint',
    severity: 'critical',
    status: 'in_progress',
    source_type: 'endpoint',
    risk_score: 92,
    created_at: '2026-02-09T04:45:00Z',
  },
  {
    id: '3',
    title: 'Data exfiltration attempt',
    description: 'Large volume of data transferred to external IP',
    severity: 'high',
    status: 'new',
    source_type: 'network',
    risk_score: 78,
    created_at: '2026-02-09T04:30:00Z',
  },
  {
    id: '4',
    title: 'Malware signature detected',
    description: 'Known malware signature identified in network traffic',
    severity: 'high',
    status: 'in_progress',
    source_type: 'ids',
    risk_score: 88,
    created_at: '2026-02-09T04:15:00Z',
  },
  {
    id: '5',
    title: 'Unauthorized API access',
    description: 'API endpoint accessed without valid credentials',
    severity: 'medium',
    status: 'new',
    source_type: 'cloud',
    risk_score: 55,
    created_at: '2026-02-09T04:00:00Z',
  },
]

export default function Alerts() {
  const [search, setSearch] = useState('')
  const [severity, setSeverity] = useState<string | null>(null)
  const [status, setStatus] = useState<string | null>(null)

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['alerts'],
    queryFn: () => alertsApi.list({ page: 1, pageSize: 20 }),
    initialData: { data: { items: mockAlerts, total: 5 } },
  })

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      case 'high':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      default:
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'new':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
      case 'in_progress':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
      case 'resolved':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Alerts</h1>
          <p className="text-muted-foreground">
            Monitor and investigate security alerts
          </p>
        </div>
        <Button onClick={() => refetch()} variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search alerts..."
                className="pl-9"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <select
                className="px-3 py-2 border rounded-md bg-background"
                value={severity || ''}
                onChange={(e) => setSeverity(e.target.value || null)}
              >
                <option value="">All Severities</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
              <select
                className="px-3 py-2 border rounded-md bg-background"
                value={status || ''}
                onChange={(e) => setStatus(e.target.value || null)}
              >
                <option value="">All Statuses</option>
                <option value="new">New</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Alerts Table */}
      <Card>
        <CardHeader>
          <CardTitle>Alert List</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.data.items.map((alert: any) => (
              <div
                key={alert.id}
                className="flex items-start justify-between p-4 border rounded-lg hover:bg-accent transition-colors"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold">{alert.title}</h3>
                    <Badge className={getSeverityColor(alert.severity)}>
                      {alert.severity}
                    </Badge>
                    <Badge className={getStatusColor(alert.status)}>
                      {alert.status.replace('_', ' ')}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">
                    {alert.description}
                  </p>
                  <div className="flex gap-4 text-xs text-muted-foreground">
                    <span>Source: {alert.source_type}</span>
                    <span>Score: {alert.risk_score}</span>
                    <span>{new Date(alert.created_at).toLocaleString()}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">
                    View
                  </Button>
                  <Button size="sm">Investigate</Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
