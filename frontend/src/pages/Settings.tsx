import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { useLanguageSelector } from '@/components/LanguageSelector'
import { Settings, Globe, Shield, Key, Webhook, Bell, Database, Save } from 'lucide-react'

// Integration placeholder configuration
interface IntegrationConfig {
  id: string
  name: string
  provider: string
  enabled: boolean
  config: Record<string, string>
}

export default function SettingsPage() {
  const { t } = useTranslation()
  const { currentLang, setLanguage } = useLanguageSelector()
  const [activeTab, setActiveTab] = useState('general')
  
  // State for settings
  const [settings, setSettings] = useState({
    theme: 'dark',
    language: currentLang.code,
    timezone: 'America/Sao_Paulo',
    email_notifications: true,
    slack_webhook: '',
    jira_url: '',
    jira_api_key: '',
    virustotal_api_key: '',
    misp_url: '',
    misp_api_key: '',
  })

  const tabs = [
    { id: 'general', label: t('settings.general'), icon: Settings },
    { id: 'integrations', label: t('settings.integrations'), icon: Globe },
    { id: 'security', label: t('roles.admin'), icon: Shield },
    { id: 'api_keys', label: 'API Keys', icon: Key },
    { id: 'webhooks', label: t('settings.webhooks'), icon: Webhook },
    { id: 'notifications', label: 'Notifications', icon: Bell },
  ]

  const handleSave = () => {
    // Save settings to API
    console.log('Saving settings:', settings)
    alert('Settings saved! (demo)')
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">{t('settings.title')}</h1>
          <p className="text-muted-foreground">
            Configure your SIEM platform
          </p>
        </div>
        <Button onClick={handleSave}>
          <Save className="h-4 w-4 mr-2" />
          {t('common.save')}
        </Button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b pb-4 overflow-x-auto">
        {tabs.map((tab) => (
          <Button
            key={tab.id}
            variant={activeTab === tab.id ? 'default' : 'ghost'}
            onClick={() => setActiveTab(tab.id)}
            className="flex items-center gap-2"
          >
            <tab.icon className="h-4 w-4" />
            {tab.label}
          </Button>
        ))}
      </div>

      {/* General Settings */}
      {activeTab === 'general' && (
        <Card>
          <CardHeader>
            <CardTitle>{t('settings.general')}</CardTitle>
            <CardDescription>
              General configuration options
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm font-medium">{t('settings.language')}</label>
                <select
                  value={settings.language}
                  onChange={(e) => {
                    setSettings({ ...settings, language: e.target.value })
                    setLanguage(e.target.value)
                  }}
                  className="w-full h-10 px-3 border rounded-md bg-background"
                >
                  <option value="en">English</option>
                  <option value="pt">Português (Brasil)</option>
                  <option value="es">Español</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium">Theme</label>
                <select
                  value={settings.theme}
                  onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
                  className="w-full h-10 px-3 border rounded-md bg-background"
                >
                  <option value="dark">Dark</option>
                  <option value="light">Light</option>
                  <option value="system">System</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium">Timezone</label>
                <select
                  value={settings.timezone}
                  onChange={(e) => setSettings({ ...settings, timezone: e.target.value })}
                  className="w-full h-10 px-3 border rounded-md bg-background"
                >
                  <option value="America/Sao_Paulo">Brasília (GMT-3)</option>
                  <option value="America/New_York">New York (GMT-5)</option>
                  <option value="Europe/London">London (GMT+0)</option>
                  <option value="Europe/Madrid">Madrid (GMT+1)</option>
                  <option value="UTC">UTC</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium">Date Format</label>
                <select className="w-full h-10 px-3 border rounded-md bg-background">
                  <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                  <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Integrations Settings */}
      {activeTab === 'integrations' && (
        <div className="grid gap-4 md:grid-cols-2">
          {/* Slack */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Slack</CardTitle>
                <Badge variant="secondary">Optional</Badge>
              </div>
              <CardDescription>
                Receive alerts and notifications in Slack
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Webhook URL</label>
                <Input
                  type="url"
                  placeholder="https://hooks.slack.com/services/..."
                  value={settings.slack_webhook}
                  onChange={(e) => setSettings({ ...settings, slack_webhook: e.target.value })}
                />
              </div>
              <Button variant="outline" size="sm" className="w-full">
                Test Connection
              </Button>
            </CardContent>
          </Card>

          {/* Jira */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Jira</CardTitle>
                <Badge variant="secondary">Optional</Badge>
              </div>
              <CardDescription>
                Create Jira tickets from cases
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Jira URL</label>
                <Input
                  type="url"
                  placeholder="https://your-domain.atlassian.net"
                  value={settings.jira_url}
                  onChange={(e) => setSettings({ ...settings, jira_url: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">API Key</label>
                <Input
                  type="password"
                  placeholder="Your Jira API Key"
                  value={settings.jira_api_key}
                  onChange={(e) => setSettings({ ...settings, jira_api_key: e.target.value })}
                />
              </div>
              <Button variant="outline" size="sm" className="w-full">
                Test Connection
              </Button>
            </CardContent>
          </Card>

          {/* VirusTotal */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>VirusTotal</CardTitle>
                <Badge variant="secondary">Optional</Badge>
              </div>
              <CardDescription>
                Threat intelligence enrichment
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">API Key</label>
                <Input
                  type="password"
                  placeholder="Your VirusTotal API Key"
                  value={settings.virustotal_api_key}
                  onChange={(e) => setSettings({ ...settings, virustotal_api_key: e.target.value })}
                />
              </div>
              <Button variant="outline" size="sm" className="w-full">
                Test Connection
              </Button>
            </CardContent>
          </Card>

          {/* MISP */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>MISP</CardTitle>
                <Badge variant="secondary">Optional</Badge>
              </div>
              <CardDescription>
                MISP Threat Intelligence Platform
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">MISP URL</label>
                <Input
                  type="url"
                  placeholder="https://misp.your-domain.com"
                  value={settings.misp_url}
                  onChange={(e) => setSettings({ ...settings, misp_url: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">API Key</label>
                <Input
                  type="password"
                  placeholder="Your MISP API Key"
                  value={settings.misp_api_key}
                  onChange={(e) => setSettings({ ...settings, misp_api_key: e.target.value })}
                />
              </div>
              <Button variant="outline" size="sm" className="w-full">
                Test Connection
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Security Settings */}
      {activeTab === 'security' && (
        <Card>
          <CardHeader>
            <CardTitle>Security Configuration</CardTitle>
            <CardDescription>
              RBAC and authentication settings
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 border rounded-lg">
              <h4 className="font-medium mb-2">Multi-Factor Authentication</h4>
              <p className="text-sm text-muted-foreground mb-3">
                Require MFA for all users (coming soon)
              </p>
              <Button variant="outline" size="sm" disabled>
                Configure MFA
              </Button>
            </div>
            
            <div className="p-4 border rounded-lg">
              <h4 className="font-medium mb-2">Session Timeout</h4>
              <p className="text-sm text-muted-foreground mb-3">
                Auto-logout after inactivity
              </p>
              <select className="w-full h-10 px-3 border rounded-md bg-background">
                <option value="15">15 minutes</option>
                <option value="30">30 minutes</option>
                <option value="60">1 hour</option>
                <option value="480">8 hours</option>
              </select>
            </div>
            
            <div className="p-4 border rounded-lg">
              <h4 className="font-medium mb-2">Password Policy</h4>
              <p className="text-sm text-muted-foreground mb-3">
                Minimum requirements for passwords
              </p>
              <div className="space-y-2">
                <label className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked />
                  <span className="text-sm">Minimum 8 characters</span>
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked />
                  <span className="text-sm">Require uppercase letters</span>
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked />
                  <span className="text-sm">Require numbers</span>
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" />
                  <span className="text-sm">Require special characters</span>
                </label>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* API Keys */}
      {activeTab === 'api_keys' && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>API Keys</CardTitle>
                <CardDescription>
                  Manage API keys for programmatic access
                </CardDescription>
              </div>
              <Button size="sm">
                <Key className="h-4 w-4 mr-2" />
                Generate New Key
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="p-4 border rounded-lg text-center text-muted-foreground">
              <Key className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No API keys generated yet</p>
              <p className="text-sm">Create an API key to enable programmatic access</p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Webhooks */}
      {activeTab === 'webhooks' && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>{t('settings.webhooks')}</CardTitle>
                <CardDescription>
                  Configure webhooks for external integrations
                </CardDescription>
              </div>
              <Button size="sm">
                <Webhook className="h-4 w-4 mr-2" />
                Add Webhook
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="p-4 border rounded-lg text-center text-muted-foreground">
              <Webhook className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No webhooks configured yet</p>
              <p className="text-sm">Create a webhook to receive real-time notifications</p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Notifications */}
      {activeTab === 'notifications' && (
        <Card>
          <CardHeader>
            <CardTitle>Notification Preferences</CardTitle>
            <CardDescription>
              Configure how you receive notifications
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-4 border rounded-lg">
              <div>
                <h4 className="font-medium">Email Notifications</h4>
                <p className="text-sm text-muted-foreground">
                  Receive alerts via email
                </p>
              </div>
              <Button
                variant={settings.email_notifications ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSettings({ 
                  ...settings, 
                  email_notifications: !settings.email_notifications 
                })}
              >
                {settings.email_notifications ? 'Enabled' : 'Disabled'}
              </Button>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-medium">Alert Types</h4>
              <div className="grid gap-2 md:grid-cols-2">
                {['Critical Alerts', 'High Alerts', 'Medium Alerts', 'Low Alerts', 'Case Updates', 'System Notifications'].map((type) => (
                  <label key={type} className="flex items-center gap-2 p-3 border rounded-lg">
                    <input type="checkbox" defaultChecked className="rounded" />
                    <span className="text-sm">{type}</span>
                  </label>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
