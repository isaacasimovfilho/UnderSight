import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Bell, AlertTriangle, Shield, Activity } from 'lucide-react'

const stats = [
  {
    name: 'Total Alerts',
    value: '1,234',
    change: '+12%',
    changeType: 'increase',
    icon: Bell,
  },
  {
    name: 'Critical',
    value: '23',
    change: '-5%',
    changeType: 'decrease',
    icon: AlertTriangle,
  },
  {
    name: 'Open Cases',
    value: '45',
    change: '+8%',
    changeType: 'increase',
    icon: Shield,
  },
  {
    name: 'Events/sec',
    value: '2.5K',
    change: '+15%',
    changeType: 'increase',
    icon: Activity,
  },
]

const recentAlerts = [
  {
    id: '1',
    title: 'Brute force attack detected',
    severity: 'high',
    source: 'Firewall',
    time: '5 minutes ago',
  },
  {
    id: '2',
    title: 'Suspicious PowerShell execution',
    severity: 'critical',
    source: 'Endpoint',
    time: '12 minutes ago',
  },
  {
    id: '3',
    title: 'Failed login attempts spike',
    severity: 'medium',
    source: 'AD',
    time: '25 minutes ago',
  },
  {
    id: '4',
    title: 'Unauthorized access attempt',
    severity: 'high',
    source: 'VPN',
    time: '1 hour ago',
  },
]

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Security overview and key metrics
        </p>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.name}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                <span
                  className={
                    stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                  }
                >
                  {stat.change}
                </span>{' '}
                from last hour
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Alerts */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Alerts</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentAlerts.map((alert) => (
              <div
                key={alert.id}
                className="flex items-center justify-between p-4 border rounded-lg"
              >
                <div className="flex items-center gap-4">
                  <div
                    className={`w-2 h-2 rounded-full ${
                      alert.severity === 'critical'
                        ? 'bg-red-500'
                        : alert.severity === 'high'
                        ? 'bg-orange-500'
                        : alert.severity === 'medium'
                        ? 'bg-yellow-500'
                        : 'bg-blue-500'
                    }`}
                  />
                  <div>
                    <p className="font-medium">{alert.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {alert.source} • {alert.time}
                    </p>
                  </div>
                </div>
                <span
                  className={`px-2 py-1 text-xs font-medium rounded-full ${
                    alert.severity === 'critical'
                      ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                      : alert.severity === 'high'
                      ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
                      : alert.severity === 'medium'
                      ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                      : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                  }`}
                >
                  {alert.severity}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Charts placeholder */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Alert Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[200px] flex items-center justify-center text-muted-foreground">
              Chart placeholder - Events over time
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Alerts by Source</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[200px] flex items-center justify-center text-muted-foreground">
              Chart placeholder - Pie chart
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
