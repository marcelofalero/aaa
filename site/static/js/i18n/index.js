/**
 * Universal i18n Translation Engine & Fallback Resolver
 * Supports infinite languages without altering core application logic.
 */
(function(global) {
  'use strict';

  global.BUILDER_I18N = global.BUILDER_I18N || {};

  /**
   * Resolves current locale from document or window environment
   */
  function getCurrentLocale() {
    if (global.AAA_CHARACTER_DATA && global.AAA_CHARACTER_DATA.lang) {
      return global.AAA_CHARACTER_DATA.lang;
    }
    return document.documentElement.lang || 'en';
  }

  /**
   * Deep key lookup inside a translation dictionary object
   */
  function getNestedValue(obj, keyPath) {
    if (!obj || typeof obj !== 'object') return null;
    const parts = keyPath.split('.');
    let curr = obj;
    for (const p of parts) {
      if (curr && typeof curr === 'object' && p in curr) {
        curr = curr[p];
      } else {
        return null;
      }
    }
    return typeof curr === 'string' ? curr : null;
  }

  /**
   * Main Translation Helper t(keyPath, fallback)
   * Lookup Order:
   * 1. Active locale dictionary (e.g., 'es', 'fr', 'de')
   * 2. Default fallback locale dictionary ('en')
   * 3. Provided explicit fallback string or keyPath
   */
  function t(keyPath, fallback = '') {
    const activeLocale = getCurrentLocale();
    const activeDict = global.BUILDER_I18N[activeLocale];
    const defaultDict = global.BUILDER_I18N['en'];

    // 1. Try active locale
    let val = getNestedValue(activeDict, keyPath);
    if (val !== null) return val;

    // 2. Try default English locale
    val = getNestedValue(defaultDict, keyPath);
    if (val !== null) return val;

    // 3. Fallback
    return fallback || keyPath;
  }

  global.tBuilder = t;
  global.getCurrentLocale = getCurrentLocale;

})(typeof window !== 'undefined' ? window : this);
