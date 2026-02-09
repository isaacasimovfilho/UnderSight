import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { assetsApi } from '@/services/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Search, RefreshCw, Activity, Shield, AlertTriangle } from 'lucide-react'

const mockAssets = [
  {
    id: '1',
    hostname: 'web-server-01',
    ip_address: '10.0.0.10',
    os: 'Ubuntu 22.04',
    asset_type: 'server',
    risk_score: 25,
    tags: ['production', 'web', 'apache'],
    last_seen: '2026-02-09T05:30:00Z',
  },
  {
    id: '2',
    hostname: 'db-server-01',
    ip_address: '10.0.0.20',
    os: 'PostgreSQL 15',
    asset_type: 'database',
    risk_score: 35,
    tags: ['production', 'database', 'critical'],
    last_seen: '2026-02-09T05:29:00Z',
  },
  {
    id: '3',
    hostname: 'workstation-win-15',
    ip_address: '10.0.1.15',
    os: 'Windows 11',
    asset_type: 'workstation',
    risk_score: 65,
    tags: ['windows', 'user-workstation'],
    last_seen: '2026-02-09T04:45:00Z',
  },
  {
    id: '4',
    hostname: 'firewall-main',
    ip_address: '10.0.0.1',
    os: 'Palo Alto PAN-OS 11',
    asset_type: 'firewall',
    risk_score: 15,
    tags: ['network', 'security', 'critical'],
    last_seen: '2026-02-09T05:30:00Z',
  },
  {
    id: '5',
    hostname: 'dev-server-03',
    ip_address: '10.0.2.30',
    os: 'Ubuntu 20.04',
    asset_type: 'server',
    risk_score: 45,
    tags: ['development', 'docker'],
    last_seen: '2026-02-09T03:00:00Z',
  },
]

export default function Assets() {
  const [search, setSearch] = useState('')

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['assets'],
    queryFn: () => assetsApi.list({ search }),
    initialData: { data: { items: mockAssets, total: 5 } },
  })

  const getRiskColor = (score: number) => {
    if (score >= 70) return 'text-red-600'
    if (score >= 50) return 'text-orange-600'
    if (score >= 30) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getAssetIcon = (type: string) => {
    switch (type) {
      case 'server':
        return <Activity className="h-5 w-5" />
      case 'workstation':
        return <Shield className="h-5 w-5" />
      case 'firewall':
        return <AlertTriangle className="h-5 w-5" />
      default:
        return <Activity className="h-5 w-5" />
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Assets</h1>
          <p className="text-muted-foreground">
            Monitor and manage your inventory
          </p>
        </div>
        <Button onClick={() => refetch()} variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Assets
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.data.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              High Risk
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">1</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Servers
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Offline
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">0</div>
          </CardContent>
        </Card>
      </div>

      {/* Search */}
      <Card>
        <CardContent className="p-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search assets by hostname, IP, or OS..."
              className="pl-9"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Assets Table */}
      <Card>
        <CardHeader>
          <CardTitle>Asset Inventory</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b text-left text-sm text-muted-foreground">
                  <th className="pb-3 font-medium">Asset</th>
                  <th className="pb-3 font-medium">IP Address</th>
                  <th className="pb-3 font-medium">OS/Type</th>
                  <th className="pb-3 font-medium">Tags</th>
                  <th className="pb-3 font-medium">Risk Score</th>
                  <th className="pb-3 font-medium">Last Seen</th>
                  <th className="pb-3 font-medium"></th>
                </tr>
              </thead>
              <tbody>
                {data.data.items.map((asset: any) => (
                  <tr key={asset.id} className="border-b last:border-0">
                    <td className="py-3">
                      <div className="flex items-center gap-2">
                        {getAssetIcon(asset.asset_type)}
                        <span className="font-medium">{asset.hostname}</span>
                      </div>
                    </td>
                    <td className="py-3 text-muted-foreground">{asset.ip_address}</td>
                    <td className="py-3 text-muted-foreground">{asset.os}</td>
                    <td className="py-3">
                      <div className="flex gap-1 flex-wrap">
                        {asset.tags.slice(0, 2).map((tag: string) => (
                          <Badge key={tag} variant="secondary">
                            {tag}
                          </Badge>
                        ))}
                        {asset.tags.length > 2 && (
                          <Badge variant="outline">+{asset.tags.length - 2}</Badge>
                        )}
                      </div>
                    </td>
                    <td className={`py-3 font-medium ${getRiskColor(asset.risk_score)}`}>
                      {asset.risk_score}
                    </td>
                    <td className="py-3 text-muted-foreground text-sm">
                      {new Date(asset.last_seen).toLocaleString()}
                    </td>
                    <td className="py-3">
                      <Button variant="outline" size="sm">
                        View
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
