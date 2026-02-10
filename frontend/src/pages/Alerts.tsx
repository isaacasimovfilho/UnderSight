import { useTranslation } from 'react-i18next'
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { alertsApi } from '@/services/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Filter, Search, RefreshCw } from 'lucide-react'

export default function Alerts() {
  const { t } = useTranslation()
  const [search, setSearch] = useState('')
  const [severity, setSeverity] = useState<string | null>(null)
  const [status, setStatus] = useState<string | null>(null)

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
          <h1 className="text-3xl font-bold">{t('alerts.title')}</h1>
          <p className="text-muted-foreground">
            {t('alerts.search')}
          </p>
        </div>
        <Button onClick={() => {}} variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          {t('common.refresh')}
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder={t('alerts.search')}
                className="pl-9"
                value={search}
                onChange={() => {}}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Alerts Table */}
      <Card>
        <CardHeader>
          <CardTitle>{t('alerts.title')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between gap-2">
              <span className="text-sm text-muted-foreground">
                {t('common.filter')}:
              </span>
              <select
                className="px-3 py-2 border rounded-md bg-background"
                value={severity || ''}
                onChange={() => setSeverity(null)}
              >
                <option value="">{t('common.all')}</option>
                <option value="critical">{t('alerts.critical')}</option>
                <option value="high">{t('alerts.high')}</option>
                <option value="medium">{t('alerts.medium')}</option>
                <option value="low">{t('alerts.low')}</option>
              </select>
              <select
                className="px-3 py-2 border rounded-md bg-background"
                value={status || ''}
                onChange={() => setStatus(null)}
              >
                <option value="">{t('alerts.all')}</option>
                <option value="new">{t('alerts.new')}</option>
                <option value="in_progress">{t('alerts.in_progress')}</option>
                <option value="resolved">{t('alerts.resolved')}</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
