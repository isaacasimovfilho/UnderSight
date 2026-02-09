import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

const resources = {
  en: {
    translation: {
      "app.name": "UnderSight",
      "app.description": "Next-Generation SIEM Platform",
      
      "nav.dashboard": "Dashboard",
      "nav.alerts": "Alerts",
      "nav.cases": "Cases",
      "nav.assets": "Assets",
      "nav.sensors": "Sensors",
      "nav.playbooks": "Playbooks",
      "nav.settings": "Settings",
      "nav.users": "Users",
      "nav.integrations": "Integrations",
      "nav.logout": "Logout",
      
      "auth.login": "Login",
      "auth.username": "Username",
      "auth.password": "Password",
      "auth.email": "Email",
      
      "dashboard.title": "Security Dashboard",
      "dashboard.total_alerts": "Total Alerts",
      "dashboard.critical_alerts": "Critical Alerts",
      "dashboard.open_cases": "Open Cases",
      
      "alerts.title": "Alerts",
      "alerts.critical": "Critical",
      "alerts.high": "High",
      "alerts.medium": "Medium",
      "alerts.low": "Low",
      
      "cases.title": "Cases",
      "cases.open": "Open",
      
      "assets.title": "Assets",
      
      "settings.title": "Settings",
      "settings.language": "Language",
      "settings.theme": "Theme",
      
      "common.save": "Save",
      "common.cancel": "Cancel",
      "common.delete": "Delete",
      "common.edit": "Edit",
      "common.create": "Create",
      "common.loading": "Loading...",
      "common.no_data": "No data available",
      
      "language.english": "English",
      "language.portuguese": "Portuguese",
      "language.spanish": "Spanish"
    }
  },
  pt: {
    translation: {
      "app.name": "UnderSight",
      "app.description": "Plataforma SIEM de Nova Geração",
      
      "nav.dashboard": "Painel",
      "nav.alerts": "Alertas",
      "nav.cases": "Casos",
      "nav.assets": "Ativos",
      "nav.sensors": "Sensores",
      "nav.playbooks": "Playbooks",
      "nav.settings": "Configurações",
      "nav.users": "Usuários",
      "nav.integrations": "Integrações",
      "nav.logout": "Sair",
      
      "auth.login": "Entrar",
      "auth.username": "Nome de usuário",
      "auth.password": "Senha",
      "auth.email": "E-mail",
      
      "dashboard.title": "Painel de Segurança",
      "dashboard.total_alerts": "Total de Alertas",
      "dashboard.critical_alerts": "Alertas Críticos",
      "dashboard.open_cases": "Casos Abertos",
      
      "alerts.title": "Alertas",
      "alerts.critical": "Crítico",
      "alerts.high": "Alto",
      "alerts.medium": "Médio",
      "alerts.low": "Baixo",
      
      "cases.title": "Casos",
      "cases.open": "Aberto",
      
      "assets.title": "Ativos",
      
      "settings.title": "Configurações",
      "settings.language": "Idioma",
      "settings.theme": "Tema",
      
      "common.save": "Salvar",
      "common.cancel": "Cancelar",
      "common.delete": "Excluir",
      "common.edit": "Editar",
      "common.create": "Criar",
      "common.loading": "Carregando...",
      "common.no_data": "Nenhum dado disponível",
      
      "language.english": "Inglês",
      "language.portuguese": "Português",
      "language.spanish": "Espanhol"
    }
  },
  es: {
    translation: {
      "app.name": "UnderSight",
      "app.description": "Plataforma SIEM de Nueva Generación",
      
      "nav.dashboard": "Panel",
      "nav.alerts": "Alertas",
      "nav.cases": "Casos",
      "nav.assets": "Activos",
      "nav.sensors": "Sensores",
      "nav.playbooks": "Playbooks",
      "nav.settings": "Configuración",
      "nav.users": "Usuarios",
      "nav.integrations": "Integraciones",
      "nav.logout": "Cerrar Sesión",
      
      "auth.login": "Iniciar Sesión",
      "auth.username": "Nombre de usuario",
      "auth.password": "Contraseña",
      "auth.email": "Correo electrónico",
      
      "dashboard.title": "Panel de Seguridad",
      "dashboard.total_alerts": "Total de Alertas",
      "dashboard.critical_alerts": "Alertas Críticos",
      "dashboard.open_cases": "Casos Abiertos",
      
      "alerts.title": "Alertas",
      "alerts.critical": "Crítico",
      "alerts.high": "Alto",
      "alerts.medium": "Medio",
      "alerts.low": "Bajo",
      
      "cases.title": "Casos",
      "cases.open": "Abierto",
      
      "assets.title": "Activos",
      
      "settings.title": "Configuración",
      "settings.language": "Idioma",
      "settings.theme": "Tema",
      
      "common.save": "Guardar",
      "common.cancel": "Cancelar",
      "common.delete": "Eliminar",
      "common.edit": "Editar",
      "common.create": "Crear",
      "common.loading": "Cargando...",
      "common.no_data": "No hay datos disponibles",
      
      "language.english": "Inglés",
      "language.portuguese": "Portugués",
      "language.spanish": "Español"
    }
  }
}

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  })

export default i18n
