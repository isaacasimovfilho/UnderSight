/**
 * Unit Tests for i18n Translations
 */

import i18n from '../i18n';

// Test translation function
const t = i18n.t.bind(i18n);

describe('i18n Translations', () => {
  beforeAll(() => {
    i18n.changeLanguage('en');
  });

  describe('App Translations', () => {
    test('app name is translated', () => {
      expect(t('app.name')).toBe('UnderSight');
    });

    test('app description is translated', () => {
      expect(t('app.description')).toBe('Next-Generation SIEM Platform');
    });
  });

  describe('Navigation Translations', () => {
    test('dashboard nav is translated', () => {
      expect(t('nav.dashboard')).toBe('Dashboard');
    });

    test('alerts nav is translated', () => {
      expect(t('nav.alerts')).toBe('Alerts');
    });

    test('cases nav is translated', () => {
      expect(t('nav.cases')).toBe('Cases');
    });

    test('assets nav is translated', () => {
      expect(t('nav.assets')).toBe('Assets');
    });

    test('settings nav is translated', () => {
      expect(t('nav.settings')).toBe('Settings');
    });

    test('inventory nav is translated', () => {
      expect(t('nav.inventory')).toBe('Inventory');
    });
  });

  describe('Auth Translations', () => {
    test('login is translated', () => {
      expect(t('auth.login')).toBe('Login');
    });

    test('username is translated', () => {
      expect(t('auth.username')).toBe('Username');
    });

    test('password is translated', () => {
      expect(t('auth.password')).toBe('Password');
    });

    test('email is translated', () => {
      expect(t('auth.email')).toBe('Email');
    });
  });

  describe('Dashboard Translations', () => {
    test('dashboard title is translated', () => {
      expect(t('dashboard.title')).toBe('Security Dashboard');
    });

    test('total alerts is translated', () => {
      expect(t('dashboard.total_alerts')).toBe('Total Alerts');
    });

    test('critical alerts is translated', () => {
      expect(t('dashboard.critical_alerts')).toBe('Critical Alerts');
    });

    test('open cases is translated', () => {
      expect(t('dashboard.open_cases')).toBe('Open Cases');
    });
  });

  describe('Alerts Translations', () => {
    test('alerts title is translated', () => {
      expect(t('alerts.title')).toBe('Alerts');
    });

    test('severity critical is translated', () => {
      expect(t('alerts.critical')).toBe('Critical');
    });

    test('severity high is translated', () => {
      expect(t('alerts.high')).toBe('High');
    });

    test('severity medium is translated', () => {
      expect(t('alerts.medium')).toBe('Medium');
    });

    test('severity low is translated', () => {
      expect(t('alerts.low')).toBe('Low');
    });
  });

  describe('Common Translations', () => {
    test('save is translated', () => {
      expect(t('common.save')).toBe('Save');
    });

    test('cancel is translated', () => {
      expect(t('common.cancel')).toBe('Cancel');
    });

    test('delete is translated', () => {
      expect(t('common.delete')).toBe('Delete');
    });

    test('edit is translated', () => {
      expect(t('common.edit')).toBe('Edit');
    });

    test('create is translated', () => {
      expect(t('common.create')).toBe('Create');
    });

    test('loading is translated', () => {
      expect(t('common.loading')).toBe('Loading...');
    });

    test('no data is translated', () => {
      expect(t('common.no_data')).toBe('No data available');
    });
  });

  describe('Language Translations', () => {
    test('english is translated', () => {
      expect(t('language.english')).toBe('English');
    });

    test('portuguese is translated', () => {
      expect(t('language.portuguese')).toBe('Portuguese');
    });

    test('spanish is translated', () => {
      expect(t('language.spanish')).toBe('Spanish');
    });
  });
});

describe('i18n Portuguese Translations', () => {
  beforeAll(() => {
    i18n.changeLanguage('pt');
  });

  test('app name is UnderSight in PT', () => {
    expect(t('app.name')).toBe('UnderSight');
  });

  test('dashboard is Painel in PT', () => {
    expect(t('nav.dashboard')).toBe('Painel');
  });

  test('alerts is Alertas in PT', () => {
    expect(t('nav.alerts')).toBe('Alertas');
  });

  test('cases is Casos in PT', () => {
    expect(t('nav.cases')).toBe('Casos');
  });

  test('save is Salvar in PT', () => {
    expect(t('common.save')).toBe('Salvar');
  });

  test('cancel is Cancelar in PT', () => {
    expect(t('common.cancel')).toBe('Cancelar');
  });
});

describe('i18n Spanish Translations', () => {
  beforeAll(() => {
    i18n.changeLanguage('es');
  });

  test('app name is UnderSight in ES', () => {
    expect(t('app.name')).toBe('UnderSight');
  });

  test('dashboard is Panel in ES', () => {
    expect(t('nav.dashboard')).toBe('Panel');
  });

  test('alerts is Alertas in ES', () => {
    expect(t('nav.alerts')).toBe('Alertas');
  });

  test('save is Guardar in ES', () => {
    expect(t('common.save')).toBe('Guardar');
  });

  test('cancel is Cancelar in ES', () => {
    expect(t('common.cancel')).toBe('Cancelar');
  });
});
