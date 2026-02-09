import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { casesApi } from '@/services/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Plus, RefreshCw, Filter } from 'lucide-react'
import { format } from 'date-fns'

const mockCases = [
  {
    id: '1',
    title: 'Ransomware Attack Investigation',
    description: 'Investigating potential ransomware infection on finance servers',
    severity: 'critical',
    status: 'open',
    priority: 1,
    assignee: 'John Doe',
    tags: ['ransomware', 'encryption', 'finance'],
    risk_score: 95,
    created_at: '2026-02-09T04:00:00Z',
    updated_at: '2026-02-09T05:30:00Z',
  },
  {
    id: '2',
    title: 'Data Breach - Customer Records',
    description: 'Investigation of unauthorized access to customer database',
    severity: 'high',
    status: 'open',
    priority: 2,
    assignee: 'Jane Smith',
    tags: ['data-breach', 'customer-data', 'unauthorized-access'],
    risk_score: 88,
    created_at: '2026-02-08T14:00:00Z',
    updated_at: '2026-02-09T03:00:00Z',
  },
  {
    id: '3',
    title: 'Insider Threat - Employee Activity',
    description: 'Analyzing unusual file downloads by former employee',
    severity: 'medium',
    status: 'in_progress',
    priority: 3,
    assignee: 'Bob Johnson',
    tags: ['insider-threat', 'data-exfiltration'],
    risk_score: 65,
    created_at: '2026-02-07T10:00:00Z',
    updated_at: '2026-02-08T16:00:00Z',
  },
]

export default function Cases() {
  const [statusFilter, setStatusFilter] = useState<string | null>(null)

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['cases'],
    queryFn: () => casesApi.list({ status: statusFilter || undefined }),
    initialData: { data: { items: mockCases, total: 3 } },
  })

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      case 'high':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow--200'
     900 dark:text-yellow default:
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
      case 'in_progress':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
      case 'resolved':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'closed':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Cases</h1>
          <p className="text-muted-foreground">
            Manage security incident investigations
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => refetch()} variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            New Case
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex gap-2">
            <Button
              variant={statusFilter === null ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter(null)}
            >
              All
            </Button>
            <Button
              variant={statusFilter === 'open' ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter('open')}
            >
              Open
            </Button>
            <Button
              variant={statusFilter === 'in_progress' ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter('in_progress')}
            >
              In Progress
            </Button>
            <Button
              variant={statusFilter === 'resolved' ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter('resolved')}
            >
              Resolved
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Cases List */}
      <div className="grid gap-4">
        {data.data.items.map((caseItem: any) => (
          <Card key={caseItem.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-2">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <CardTitle className="text-lg">{caseItem.title}</CardTitle>
                  <Badge className={getSeverityColor(caseItem.severity)}>
                    {caseItem.severity}
                  </Badge>
                  <Badge className={getStatusColor(caseItem.status)}>
                    {caseItem.status.replace('_', ' ')}
                  </Badge>
                </div>
                <span className="text-sm text-muted-foreground">
                  #{caseItem.id.slice(0, 8)}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                {caseItem.description}
              </p>
              <div className="flex flex-wrap gap-2 mb-3">
                {caseItem.tags.map((tag: string) => (
                  <Badge key={tag} variant="secondary">
                    {tag}
                  </Badge>
                ))}
              </div>
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <div className="flex gap-4">
                  <span>Assignee: {caseItem.assignee}</span>
                  <span>Priority: P{caseItem.priority}</span>
                  <span>Risk: {caseItem.risk_score}</span>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">
                    View
                  </Button>
                  <Button size="sm">Investigate</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
