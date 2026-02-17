import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

void i18n.use(initReactI18next).init({
  lng: 'ru',
  fallbackLng: 'en',
  resources: {
    ru: { translation: { login: 'Войти', plants: 'Растения', addPlant: 'Добавить растение' } },
    en: { translation: { login: 'Login', plants: 'Plants', addPlant: 'Add plant' } }
  }
});

export default i18n;
