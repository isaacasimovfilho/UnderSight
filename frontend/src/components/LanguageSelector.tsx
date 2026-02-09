import { useEffect } from 'react'
import { useTranslation } from 'react-i18next'

// Language data
export const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'pt', name: 'Português', flag: '🇧🇷' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
]

// Hook to get current language
export function useLanguage() {
  const { i18n } = useTranslation()
  
  const currentLang = languages.find(l => l.code === i18n.language) || languages[0]
  
  const setLanguage = (code: string) => {
    i18n.changeLanguage(code)
    localStorage.setItem('lang', code)
    document.documentElement.lang = code
  }
  
  return {
    currentLang,
    setLanguage,
    supportedLanguages: languages
  }
}

// Component: Language Selector
export function LanguageSelector({ className = '' }: { className?: string }) {
  const { t, i18n } = useTranslation()
  const { currentLang, setLanguage, supportedLanguages } = useLanguage()
  
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-lg">{currentLang.flag}</span>
      <select
        value={currentLang.code}
        onChange={(e) => setLanguage(e.target.value)}
        className="bg-background border rounded-md px-2 py-1 text-sm"
      >
        {supportedLanguages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  )
}

// Initialize language on app start
export function initLanguage() {
  const savedLang = localStorage.getItem('lang')
  const browserLang = navigator.language.split('-')[0]
  
  const lang = savedLang || 
    (['en', 'pt', 'es'].includes(browserLang) ? browserLang : 'en')
  
  i18n.changeLanguage(lang)
  document.documentElement.lang = lang
  
  return lang
}

export default LanguageSelector
