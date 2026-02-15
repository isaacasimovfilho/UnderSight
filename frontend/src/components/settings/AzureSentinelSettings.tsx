import React, { useState, useEffect } from 'react';
import { useLanguage } from '../LanguageSelector';
import { useAuth } from '../../stores/auth';

// Types
interface AzureConfig {
  tenant_id: string;
  client_id: string;
  client_secret: string;
  subscription_id: string;
  workspace_name: string;
}

interface AzureStats {
  status: string;
  message: string;
  configured: boolean;
  events_fetched?: number;
  events_indexed?: number;
  last_sync?: string;
}

interface SyncStatus {
  enabled: boolean;
  scheduler_running: boolean;
  sync_interval_minutes: number;
}

const translations = {
  en: {
    title: 'Azure Sentinel Integration',
    description: 'Configure Microsoft Sentinel to collect security events',
    tenantId: 'Tenant ID',
    clientId: 'Client ID',
    clientSecret: 'Client Secret',
    subscriptionId: 'Subscription ID',
    workspaceName: 'Workspace Name',
    save: 'Save Configuration',
    testing: 'Testing connection...',
    connected: '✅ Connected to Azure Sentinel',
    failed: '❌ Connection failed',
    notConfigured: '⚠️ Not configured',
    syncStatus: 'Sync Status',
    enabled: 'Enabled',
    disabled: 'Disabled',
    running: 'Running',
    stopped: 'Stopped',
    interval: 'Sync Interval',
    minutes: 'minutes',
    startSync: 'Start Auto Sync',
    stopSync: 'Stop Auto Sync',
    triggerSync: 'Trigger Now',
    stats: 'Integration Stats',
    eventsFetched: 'Events Fetched',
    eventsIndexed: 'Events Indexed',
    lastSync: 'Last Sync',
    never: 'Never',
    testConnection: 'Test Connection',
  },
  pt: {
    title: 'Integração Azure Sentinel',
    description: 'Configure o Microsoft Sentinel para coletar eventos de segurança',
    tenantId: 'Tenant ID',
    clientId: 'Client ID',
    clientSecret: 'Client Secret',
    subscriptionId: 'Subscription ID',
    workspaceName: 'Workspace Name',
    save: 'Salvar Configuração',
    testing: 'Testando conexão...',
    connected: '✅ Conectado ao Azure Sentinel',
    failed: '❌ Falha na conexão',
    notConfigured: '⚠️ Não configurado',
    syncStatus: 'Status do Sync',
    enabled: 'Ativado',
    disabled: 'Desativado',
    running: 'Em execução',
    stopped: 'Parado',
    interval: 'Intervalo de Sync',
    minutes: 'minutos',
    startSync: 'Iniciar Sync Automático',
    stopSync: 'Parar Sync Automático',
    triggerSync: 'Sincronizar Agora',
    stats: 'Estatísticas da Integração',
    eventsFetched: 'Eventos Recebidos',
    eventsIndexed: 'Eventos Indexados',
    lastSync: 'Último Sync',
    never: 'Nunca',
    testConnection: 'Testar Conexão',
  },
  es: {
    title: 'Integración Azure Sentinel',
    description: 'Configure Microsoft Sentinel para recopilar eventos de seguridad',
    tenantId: 'Tenant ID',
    clientId: 'Client ID',
    clientSecret: 'Client Secret',
    subscriptionId: 'Subscription ID',
    workspaceName: 'Workspace Name',
    save: 'Guardar Configuración',
    testing: 'Probando conexión...',
    connected: '✅ Conectado a Azure Sentinel',
    failed: '❌ Error de conexión',
    notConfigured: '⚠️ No configurado',
    syncStatus: 'Estado de Sincronización',
    enabled: 'Activado',
    disabled: 'Desactivado',
    running: 'Ejecutando',
    stopped: 'Detenido',
    interval: 'Intervalo de Sync',
    minutes: 'minutos',
    startSync: 'Iniciar Sync Automático',
    stopSync: 'Detener Sync Automático',
    triggerSync: 'Sincronizar Ahora',
    stats: 'Estadísticas de Integración',
    eventsFetched: 'Eventos Recibidos',
    eventsIndexed: 'Eventos Indexados',
    lastSync: 'Última Sincronización',
    never: 'Nunca',
    testConnection: 'Probar Conexión',
  },
};

export default function AzureSentinelSettings() {
  const { language } = useLanguage();
  const { api } = useAuth();
  const t = translations[language as keyof typeof translations] || translations.en;

  const [config, setConfig] = useState<AzureConfig>({
    tenant_id: '',
    client_id: '',
    client_secret: '',
    subscription_id: '',
    workspace_name: '',
  });

  const [status, setStatus] = useState<AzureStats | null>(null);
  const [syncStatus, setSyncStatus] = useState<SyncStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Load saved config from backend
  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    try {
      const [statusRes, syncRes] = await Promise.all([
        api.get('/api/v1/azure/status'),
        api.get('/api/v1/azure/sync/status'),
      ]);

      setStatus(statusRes.data);
      setSyncStatus(syncRes.data);

      // Load env vars as default config (masked)
      setConfig({
        tenant_id: statusRes.data.configured ? '••••••••-••••-••••-••••-••••••••••••' : '',
        client_id: statusRes.data.configured ? '••••••••-••••-••••-••••-••••••••••••' : '',
        client_secret: '••••••••••••••••••••••••••••••••',
        subscription_id: statusRes.data.configured ? '••••••••-••••-••••-••••-••••••••••••' : '',
        workspace_name: statusRes.data.configured ? 'sentinel-teste' : '',
      });
    } catch (error) {
      console.error('Failed to load Azure status:', error);
    }
  };

  const testConnection = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const response = await api.get('/api/v1/azure/status');
      setStatus(response.data);
      if (response.data.status === 'connected') {
        setMessage({ type: 'success', text: t.connected });
      } else {
        setMessage({ type: 'error', text: t.failed });
      }
    } catch (error: any) {
      setMessage({ type: 'error', text: error.response?.data?.detail || t.failed });
    }
    setLoading(false);
  };

  const saveConfig = async () => {
    setLoading(true);
    setMessage(null);
    try {
      await api.post('/api/v1/azure/configure', {
        tenant_id: config.tenant_id.replace(/•/g, ''),
        client_id: config.client_id.replace(/•/g, ''),
        client_secret: config.client_secret.replace(/•/g, ''),
        subscription_id: config.subscription_id.replace(/•/g, ''),
        workspace_name: config.workspace_name,
      });
      setMessage({ type: 'success', text: '✅ Configuration saved!' });
      loadStatus();
    } catch (error: any) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Error saving configuration' });
    }
    setLoading(false);
  };

  const startSync = async () => {
    try {
      await api.post('/api/v1/azure/sync/start');
      loadStatus();
      setMessage({ type: 'success', text: '✅ Sync started!' });
    } catch (error: any) {
      setMessage({ type: 'error', text: 'Error starting sync' });
    }
  };

  const stopSync = async () => {
    try {
      await api.post('/api/v1/azure/sync/stop');
      loadStatus();
      setMessage({ type: 'success', text: '✅ Sync stopped!' });
    } catch (error: any) {
      setMessage({ type: 'error', text: 'Error stopping sync' });
    }
  };

  const triggerSync = async () => {
    setLoading(true);
    try {
      await api.post('/api/v1/azure/sync/trigger');
      loadStatus();
      setMessage({ type: 'success', text: '✅ Sync completed!' });
    } catch (error: any) {
      setMessage({ type: 'error', text: 'Error triggering sync' });
    }
    setLoading(false);
  };

  const inputClass = "w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 text-sm";
  const labelClass = "block text-xs text-gray-400 mb-1 uppercase tracking-wide";

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold text-white mb-2">{t.title}</h2>
      <p className="text-gray-400 text-sm mb-6">{t.description}</p>

      {/* Connection Status */}
      <div className="mb-6 p-4 bg-gray-900 rounded-lg border border-gray-700">
        <div className="flex items-center justify-between">
          <div>
            <span className="text-sm text-gray-400">{t.syncStatus}: </span>
            <span className={status?.status === 'connected' ? 'text-green-400' : 'text-yellow-400'}>
              {status?.status === 'connected' ? t.enabled : t.notConfigured}
            </span>
          </div>
          <button
            onClick={testConnection}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm font-medium transition-colors disabled:opacity-50"
          >
            {loading ? t.testing : t.testConnection}
          </button>
        </div>

        {message && (
          <div className={`mt-3 p-2 rounded text-sm ${message.type === 'success' ? 'bg-green-900/50 text-green-400' : 'bg-red-900/50 text-red-400'}`}>
            {message.text}
          </div>
        )}
      </div>

      {/* Configuration Form */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-300 mb-4 uppercase tracking-wide">Configuration</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>{t.tenantId}</label>
            <input
              type="text"
              value={config.tenant_id}
              onChange={(e) => setConfig({ ...config, tenant_id: e.target.value })}
              className={inputClass}
              placeholder="76b9a5c2-4daa-454d-b18d-a5dc8cfb3191"
            />
          </div>
          <div>
            <label className={labelClass}>{t.clientId}</label>
            <input
              type="text"
              value={config.client_id}
              onChange={(e) => setConfig({ ...config, client_id: e.target.value })}
              className={inputClass}
              placeholder="eaf1bc9f-b6a7-4df1-9b5e-8ab5586c2eea"
            />
          </div>
          <div>
            <label className={labelClass}>{t.clientSecret}</label>
            <input
              type="password"
              value={config.client_secret}
              onChange={(e) => setConfig({ ...config, client_secret: e.target.value })}
              className={inputClass}
              placeholder="••••••••••••••••••••••••••••••••"
            />
          </div>
          <div>
            <label className={labelClass}>{t.subscriptionId}</label>
            <input
              type="text"
              value={config.subscription_id}
              onChange={(e) => setConfig({ ...config, subscription_id: e.target.value })}
              className={inputClass}
              placeholder="c9082f04-e702-44dd-abd3-c561286e3c11"
            />
          </div>
          <div className="md:col-span-2">
            <label className={labelClass}>{t.workspaceName}</label>
            <input
              type="text"
              value={config.workspace_name}
              onChange={(e) => setConfig({ ...config, workspace_name: e.target.value })}
              className={inputClass}
              placeholder="sentinel-workspace"
            />
          </div>
        </div>

        <button
          onClick={saveConfig}
          disabled={loading}
          className="mt-4 px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded text-sm font-medium transition-colors disabled:opacity-50"
        >
          {t.save}
        </button>
      </div>

      {/* Sync Settings */}
      <div className="mb-6 p-4 bg-gray-900 rounded-lg border border-gray-700">
        <h3 className="text-sm font-semibold text-gray-300 mb-4 uppercase tracking-wide">{t.syncStatus}</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <span className="text-gray-400 text-sm">{t.enabled}: </span>
            <span className={syncStatus?.enabled ? 'text-green-400' : 'text-red-400'}>
              {syncStatus?.enabled ? t.enabled : t.disabled}
            </span>
          </div>
          <div>
            <span className="text-gray-400 text-sm">{t.running}: </span>
            <span className={syncStatus?.scheduler_running ? 'text-green-400' : 'text-yellow-400'}>
              {syncStatus?.scheduler_running ? t.running : t.stopped}
            </span>
          </div>
          <div>
            <span className="text-gray-400 text-sm">{t.interval}: </span>
            <span className="text-white">{syncStatus?.sync_interval_minutes} {t.minutes}</span>
          </div>
        </div>

        <div className="flex gap-2">
          {syncStatus?.scheduler_running ? (
            <button
              onClick={stopSync}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded text-sm font-medium transition-colors"
            >
              {t.stopSync}
            </button>
          ) : (
            <button
              onClick={startSync}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded text-sm font-medium transition-colors"
            >
              {t.startSync}
            </button>
          )}
          <button
            onClick={triggerSync}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm font-medium transition-colors disabled:opacity-50"
          >
            {t.triggerSync}
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="p-4 bg-gray-900 rounded-lg border border-gray-700">
        <h3 className="text-sm font-semibold text-gray-300 mb-4 uppercase tracking-wide">{t.stats}</h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-gray-800 rounded">
            <div className="text-2xl font-bold text-blue-400">{status?.events_fetched || 0}</div>
            <div className="text-xs text-gray-500">{t.eventsFetched}</div>
          </div>
          <div className="text-center p-3 bg-gray-800 rounded">
            <div className="text-2xl font-bold text-green-400">{status?.events_indexed || 0}</div>
            <div className="text-xs text-gray-500">{t.eventsIndexed}</div>
          </div>
          <div className="text-center p-3 bg-gray-800 rounded">
            <div className="text-2xl font-bold text-purple-400">{syncStatus?.sync_interval_minutes || 0}</div>
            <div className="text-xs text-gray-500">{t.minutes}</div>
          </div>
          <div className="text-center p-3 bg-gray-800 rounded">
            <div className="text-2xl font-bold text-yellow-400">{status?.last_sync ? new Date(status.last_sync).toLocaleTimeString() : t.never}</div>
            <div className="text-xs text-gray-500">{t.lastSync}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
