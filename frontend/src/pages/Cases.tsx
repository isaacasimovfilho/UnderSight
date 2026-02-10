import { useTranslation } from 'react-i18next'
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { casesApi } from '@/services/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Plus, RefreshCw, Filter } from 'lucide-react'

export default function Cases() {
  const { t } = useTranslation()
  const [statusFilter, setStatusFilter] = useState<string | null>(null)

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
          <h1 className="text-3xl font-bold">{t('cases.title')}</h1>
          <p className="text-muted-foreground">
            {t('cases.create')}
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => {}} variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            {t('common.refresh')}
          </Button>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            {t('cases.new')}
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
              {t('common.all')}
            </Button>
            <Button
              variant={statusFilter === 'open' ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter('open')}
            >
              {t('cases.open')}
            </Button>
            <Button
              variant={statusFilter === 'in_progress' ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter('in_progress')}
            >
              {t('cases.investigating')}
            </Button>
            <Button
              variant={statusFilter === 'resolved' ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter('resolved')}
            >
              {t('cases.resolved')}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Cases List */}
      <Card>
        <CardHeader>
          <CardTitle>{t('cases.title')}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            {t('cases.no_cases')}
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
