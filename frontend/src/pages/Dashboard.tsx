import { useTranslation } from 'react-i18next'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Bell, AlertTriangle, Shield, Activity } from 'lucide-react'

export default function Dashboard() {
  const { t } = useTranslation()
  
  const stats = [
    {
      name: t('dashboard.total_alerts'),
      value: '1,234',
      change: '+12%',
      changeType: 'increase',
      icon: Bell,
    },
    {
      name: t('dashboard.critical_alerts'),
      value: '23',
      change: '-5%',
      changeType: 'decrease',
      icon: AlertTriangle,
    },
    {
      name: t('dashboard.open_cases'),
      value: '45',
      change: '+8%',
      changeType: 'increase',
      icon: Shield,
    },
    {
      name: t('dashboard.events_per_second'),
      value: '2.5K',
      change: '+15%',
      changeType: 'increase',
      icon: Activity,
    },
  ]
  
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">{t('dashboard.title')}</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
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
                {stat.change} from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
