import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './locales/en.json';
import hi from './locales/hi.json';

const resources = {
  en: { translation: en },
  hi: { translation: hi },
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en', // Default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

// Handle language change side-effects (Devanagari font loading & line height adjustment per Design.md Section 5)
i18n.on('languageChanged', (lng) => {
  document.documentElement.setAttribute('lang', lng);
  if (lng === 'hi') {
    document.body.classList.add('font-devanagari');
  } else {
    document.body.classList.remove('font-devanagari');
  }
});

export default i18n;
