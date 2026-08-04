import { useTranslation } from 'react-i18next';

export function usei18n() {
  const { t, i18n } = useTranslation();
  
  const changeLanguage = (lng: 'en' | 'hi') => {
    i18n.changeLanguage(lng);
  };

  return {
    t,
    currentLanguage: i18n.language as 'en' | 'hi',
    changeLanguage,
  };
}
