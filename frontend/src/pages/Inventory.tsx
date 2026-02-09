import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { DataTable } from '@/components/ui/data-table'
import { 
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from '@/components/ui/table'
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, 
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import { Check, X, Flag, MoreHorizontal, Search, Filter, Download, Upload } from 'lucide-react'

// API functions
const fetchInventory = async (params: any) => {
  const response = await fetch(`/api/v1/inventory/items?${new URLSearchParams(params)}`)
  return response.json()
}

const approveItem = async (id: string) => {
  const response = await fetch(`/api/v1/inventory/items/${id}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
  })
  return response.json()
}

const rejectItem = async (id: string) => {
  const response = await fetch(`/api/v1/inventory/items/${id}/reject`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
  })
  return response.json()
}

export default function InventoryPage() {
  const { t } = useTranslation()
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState<string | null>(null)
  const [assetTypeFilter, setAssetTypeFilter] = useState<string | null>(null)
  
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['inventory', { search, statusFilter, assetTypeFilter }],
    queryFn: () => fetchInventory({
      search: search || undefined,
      status: statusFilter || undefined,
      asset_type: assetTypeFilter || undefined,
      page: 1,
      page_size: 50
    })
  })
  
  const approveMutation = useMutation({
    mutationFn: approveItem,
    onSuccess: () => refetch()
  })
  
  const rejectMutation = useMutation({
    mutationFn: rejectItem,
    onSuccess: () => refetch()
  })
  
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'approved':
        return <Badge className="bg-green-500">Approved</Badge>
      case 'rejected':
        return <Badge variant="destructive">Rejected</Badge>
      case 'pending':
        return <Badge variant="warning">Pending</Badge>
      case 'flag':
        return <Badge variant="secondary">Flagged</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Inventory</h1>
          <p className="text-muted-foreground">
            AI-powered equipment inventory management
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline className="h">
            <Upload-4 w-4 mr-2" />
            Import from N8N
          </Button>
          <Button>
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Items
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data?.total || 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Pending Review
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-500">
              {data?.items?.filter((i: any) => i.status === 'pending').length || 0}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Approved
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-500">
              {data?.items?.filter((i: any) => i.status === 'approved').length || 0}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Rejected
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">
              {data?.items?.filter((i: any) => i.status === 'rejected').length || 0}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search by hostname, IP, or owner..."
                className="pl-9"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <select
              className="px-3 py-2 border rounded-md bg-background"
              value={statusFilter || ''}
              onChange={(e) => setStatusFilter(e.target.value || null)}
            >
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
              <option value="flag">Flagged</option>
            </select>
            <select
              className="px-3 py-2 border rounded-md bg-background"
              value={assetTypeFilter || ''}
              onChange={(e) => setAssetTypeFilter(e.target.value || null)}
            >
              <option value="">All Types</option>
              <option value="server">Server</option>
              <option value="workstation">Workstation</option>
              <option value="network">Network</option>
              <option value="cloud">Cloud</option>
              <option value="iot">IoT</option>
            </select>
            <Button variant="outline" onClick={() => refetch()}>
              <Filter className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Inventory Table */}
      <Card>
        <CardHeader>
          <CardTitle>Equipment Inventory</CardTitle>
          <CardDescription>
            Items received from N8N and processed by AI
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Hostname</TableHead>
                  <TableHead>IP Address</TableHead>
                  <TableHead>OS</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Source</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>AI Decision</TableHead>
                  <TableHead>Risk</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  <TableRow>
                    <TableCell colSpan={9} className="text-center py-8">
                      Loading...
                    </TableCell>
                  </TableRow>
                ) : data?.items?.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={9} className="text-center py-8 text-muted-foreground">
                      No inventory items found
                    </TableCell>
                  </TableRow>
                ) : (
                  data?.items?.map((item: any) => (
                    <TableRow key={item.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{item.hostname || 'Unknown'}</div>
                          <div className="text-xs text-muted-foreground">
                            {item.manufacturer} {item.model}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>{item.ip_address || '-'}</TableCell>
                      <TableCell>
                        <div>
                          <div>{item.os || 'Unknown'}</div>
                          {item.os_version && (
                            <div className="text-xs text-muted-foreground">{item.os_version}</div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">{item.asset_type || '-'}</Badge>
                      </TableCell>
                      <TableCell>{item.source}</TableCell>
                      <TableCell>{getStatusBadge(item.status)}</TableCell>
                      <TableCell>
                        <div className="max-w-xs truncate text-sm" title={item.inventory_decision}>
                          {item.inventory_decision || '-'}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className={`text-sm font-medium ${
                          item.risk_score >= 70 ? 'text-red-500' :
                          item.risk_score >= 40 ? 'text-yellow-500' :
                          'text-green-500'
                        }`}>
                          {item.risk_score}
                        </div>
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => approveMutation.mutate(item.id)}>
                              <Check className="h-4 w-4 mr-2" />
                              Approve
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => rejectMutation.mutate(item.id)}>
                              <X className="h-4 w-4 mr-2" />
                              Reject
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Flag className="h-4 w-4 mr-2" />
                              Flag for Review
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* AI Processing Info */}
      <Card>
        <CardHeader>
          <CardTitle>AI Processing</CardTitle>
          <CardDescription>
            Configure how AI processes incoming equipment
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="p-4 border rounded-lg">
              <h4 className="font-medium mb-2">N8N Webhook</h4>
              <code className="text-sm bg-muted p-2 rounded block">
                /api/v1/inventory/webhook/n8n
              </code>
              <p className="text-xs text-muted-foreground mt-2">
                Configure this URL in N8N to send equipment data
              </p>
            </div>
            <div className="p-4 border rounded-lg">
              <h4 className="font-medium mb-2">AI Providers</h4>
              <div className="flex flex-wrap gap-1">
                <Badge variant="outline">OpenAI</Badge>
                <Badge variant="outline">Anthropic</Badge>
                <Badge variant="outline">Ollama</Badge>
                <Badge variant="outline">Groq</Badge>
                <Badge variant="outline">DeepSeek</Badge>
              </div>
            </div>
            <div className="p-4 border rounded-lg">
              <h4 className="font-medium mb-2">Processing Time</h4>
              <div className="text-2xl font-bold">~2-5s</div>
              <p className="text-xs text-muted-foreground">
                Average AI processing time per item
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
