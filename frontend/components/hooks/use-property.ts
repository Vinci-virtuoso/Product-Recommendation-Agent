import { useState, useCallback } from 'react';

export function useProperty() {
  const [savedProperties, setSavedProperties] = useState<number[]>([]);

  const isPropertySaved = useCallback((productId: number) => {
    return savedProperties.includes(productId);
  }, [savedProperties]);

  const toggleSaveProperty = useCallback((productId: number) => {
    setSavedProperties(prev => {
      if (prev.includes(productId)) {
        return prev.filter(id => id !== productId);
      }
      return [...prev, productId];
    });
  }, []);

  return {
    isPropertySaved,
    toggleSaveProperty,
    savedProperties
  };
}
