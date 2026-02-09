# i18n Configuration for UnderSight
# Internationalization support

from typing import Dict, Any
import json
import os
from pathlib import Path

# Default language
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "pt", "es"]

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Translations cache
_translations: Dict[str, Dict[str, str]] = {}


def load_translations(lang: str) -> Dict[str, str]:
    """Load translation file for a language."""
    if lang in _translations:
        return _translations[lang]
    
    translations_file = BASE_DIR / "locales" / f"{lang}.json"
    
    if translations_file.exists():
        with open(translations_file, 'r', encoding='utf-8') as f:
            _translations[lang] = json.load(f)
    else:
        # Fallback to English
        _translations[lang] = {}
    
    return _translations[lang]


def get_translation(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """Get translated string."""
    translations = load_translation(lang)
    
    text = translations.get(key, key)
    
    # Replace placeholders
    for placeholder, value in kwargs.items():
        text = text.replace(f"{{{{ {placeholder} }}}}", str(value))
        text = text.replace(f"{{{placeholder}}}", str(value))
    
    return text


class I18nMiddleware:
    """Middleware to add language detection and translation support."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get language from header, cookie, or query parameter
        lang = self.get_language(request)
        request.i18n_lang = lang
        
        response = self.get_response(request)
        response.headers['Content-Language'] = lang
        return response
    
    def get_language(self, request) -> str:
        """Determine language from request."""
        # Check query parameter
        lang = request.query_params.get('lang')
        if lang and lang in SUPPORTED_LANGUAGES:
            return lang
        
        # Check header
        accept_language = request.headers.get('Accept-Language', '')
        if accept_language:
            for lang in SUPPORTED_LANGUAGES:
                if lang in accept_language.lower():
                    return lang
        
        # Check cookie
        lang = request.cookies.get('lang')
        if lang and lang in SUPPORTED_LANGUAGES:
            return lang
        
        return DEFAULT_LANGUAGE


# Translation function shortcut
def _(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """Translate a string."""
    return get_translation(key, lang, **kwargs)


# Response messages
MESSAGES = {
    "en": {
        "auth.login_success": "Login successful",
        "auth.login_failed": "Invalid credentials",
        "auth.token_expired": "Token has expired",
        "auth.token_invalid": "Invalid token",
        "auth.unauthorized": "Unauthorized access",
        "auth.forbidden": "Access forbidden",
        "alerts.created": "Alert created successfully",
        "alerts.updated": "Alert updated successfully",
        "alerts.deleted": "Alert deleted successfully",
        "cases.created": "Case created successfully",
        "cases.updated": "Case updated successfully",
        "cases.closed": "Case closed successfully",
        "cases.assigned": "Case assigned successfully",
        "users.created": "User created successfully",
        "users.updated": "User updated successfully",
        "users.deleted": "User deleted successfully",
        "users.inactive": "User account is inactive",
        "tenants.switched": "Tenant switched successfully",
        "permissions.denied": "Permission denied",
        "integrations.configured": "Integration configured successfully",
        "integrations.test_success": "Integration test successful",
        "integrations.test_failed": "Integration test failed",
        "errors.validation": "Validation error",
        "errors.not_found": "Resource not found",
        "errors.internal": "Internal server error",
    },
    "pt": {
        "auth.login_success": "Login realizado com sucesso",
        "auth.login_failed": "Credenciais inválidas",
        "auth.token_expired": "Token expirado",
        "auth.token_invalid": "Token inválido",
        "auth.unauthorized": "Acesso não autorizado",
        "auth.forbidden": "Acesso proibido",
        "alerts.created": "Alerta criado com sucesso",
        "alerts.updated": "Alerta atualizado com sucesso",
        "alerts.deleted": "Alerta excluído com sucesso",
        "cases.created": "Caso criado com sucesso",
        "cases.updated": "Caso atualizado com sucesso",
        "cases.closed": "Caso fechado com sucesso",
        "cases.assigned": "Caso atribuído com sucesso",
        "users.created": "Usuário criado com sucesso",
        "users.updated": "Usuário atualizado com sucesso",
        "users.deleted": "Usuário excluído com sucesso",
        "users.inactive": "Conta de usuário está inativa",
        "tenants.switched": "Locatário alterado com sucesso",
        "permissions.denied": "Permissão negada",
        "integrations.configured": "Integração configurada com sucesso",
        "integrations.test_success": "Teste de integração bem-sucedido",
        "integrations.test_failed": "Falha no teste de integração",
        "errors.validation": "Erro de validação",
        "errors.not_found": "Recurso não encontrado",
        "errors.internal": "Erro interno do servidor",
    },
    "es": {
        "auth.login_success": "Inicio de sesión exitoso",
        "auth.login_failed": "Credenciales inválidas",
        "auth.token_expired": "Token ha expirado",
        "auth.token_invalid": "Token inválido",
        "auth.unauthorized": "Acceso no autorizado",
        "auth.forbidden": "Acceso prohibido",
        "alerts.created": "Alerta creado exitosamente",
        "alerts.updated": "Alerta actualizado exitosamente",
        "alerts.deleted": "Alerta eliminado exitosamente",
        "cases.created": "Caso creado exitosamente",
        "cases.updated": "Caso actualizado exitosamente",
        "cases.closed": "Caso cerrado exitosamente",
        "cases.assigned": "Caso asignado exitosamente",
        "users.created": "Usuario creado exitosamente",
        "users.updated": "Usuario actualizado exitosamente",
        "users.deleted": "Usuario eliminado exitosamente",
        "users.inactive": "La cuenta de usuario está inactiva",
        "tenants.switched": "Inquilino cambiado exitosamente",
        "permissions.denied": "Permiso denegado",
        "integrations.configured": "Integración configurada exitosamente",
        "integrations.test_success": "Prueba de integración exitosa",
        "integrations.test_failed": "Error en prueba de integración",
        "errors.validation": "Error de validación",
        "errors.not_found": "Recurso no encontrado",
        "errors.internal": "Error interno del servidor",
    }
}


def get_message(key: str, lang: str = DEFAULT_LANGUAGE) -> str:
    """Get a translated message."""
    return MESSAGES.get(lang, MESSAGES.get(DEFAULT_LANGUAGE, {})).get(key, key)
