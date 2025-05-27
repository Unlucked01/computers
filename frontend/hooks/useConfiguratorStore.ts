import { create } from 'zustand';
import { Component, Configuration, ConfiguratorState, CompatibilityCheck } from '../types';
import { checkCompatibilityAPI, configurationsApi } from '../lib/api';

interface ConfiguratorStore extends ConfiguratorState {
  // Actions
  addComponent: (component: Component) => void;
  removeComponent: (categorySlug: string) => void;
  clearConfiguration: () => void;
  checkCompatibility: () => Promise<void>;
  saveConfiguration: (name: string, description?: string) => Promise<void>;
  addAccessoriesToConfiguration: (accessories: Array<{component: Component, quantity: number}>) => Promise<void>;
  exportToPdf: () => Promise<Blob | null>;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useConfiguratorStore = create<ConfiguratorStore>((set, get) => ({
  // Initial state
  selectedComponents: {},
  currentConfiguration: undefined,
  isLoading: false,
  error: undefined,

  // Actions
  addComponent: (component: Component) => {
    const state = get();
    const newSelectedComponents = {
      ...state.selectedComponents,
      [component.category.slug]: component,
    };

    set({
      selectedComponents: newSelectedComponents,
      error: undefined,
    });
  },

  removeComponent: (categorySlug: string) => {
    const state = get();
    const newSelectedComponents = { ...state.selectedComponents };
    delete newSelectedComponents[categorySlug];

    set({
      selectedComponents: newSelectedComponents,
      error: undefined,
    });
  },

  clearConfiguration: () => {
    set({
      selectedComponents: {},
      currentConfiguration: undefined,
      error: undefined,
    });
  },

  checkCompatibility: async () => {
    const state = get();
    const componentIds = Object.values(state.selectedComponents).map(c => c.id);
    
    if (componentIds.length < 2) {
      return; // Не проверяем совместимость для менее чем 2 компонентов
    }

    set({ isLoading: true });

    try {
      const compatibilityResult = await checkCompatibilityAPI(componentIds);
      
      // Обновляем конфигурацию с результатами проверки совместимости
      const newConfiguration: Configuration = {
        id: '0',
        name: 'Текущая конфигурация',
        description: '',
        total_price: Object.values(state.selectedComponents).reduce((sum, c) => sum + c.price, 0),
        currency: 'RUB',
        status: 'draft',
        compatibility_status: compatibilityResult.status,
        compatibility_issues: compatibilityResult.issues,
        availability_status: 'unknown',
        created_at: new Date().toISOString(),
        items: Object.values(state.selectedComponents).map((component, index) => ({
          id: `temp-${index}`,
          component,
          quantity: 1,
          price_snapshot: component.price,
          order_priority: index,
          added_at: new Date().toISOString(),
        })),
      };

      set({
        currentConfiguration: newConfiguration,
        isLoading: false,
        error: undefined,
      });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Ошибка проверки совместимости',
      });
    }
  },

  saveConfiguration: async (name: string, description?: string) => {
    const state = get();
    const components = Object.values(state.selectedComponents);
    
    if (components.length === 0) {
      set({ error: 'Нет компонентов для сохранения' });
      return;
    }

    set({ isLoading: true });

    try {
      // 1. Создаем базовую конфигурацию
      const savedConfig = await configurationsApi.create({
        name,
        description,
      });

      // 2. Добавляем каждый компонент в конфигурацию
      for (const component of components) {
        await configurationsApi.addComponent(savedConfig.id, component.id, 1);
      }

      // 3. Проверяем совместимость сохраненной конфигурации
      const compatibilityResult = await configurationsApi.checkCompatibility(savedConfig.id);

      // 4. Получаем обновленную конфигурацию
      const updatedConfig = await configurationsApi.getById(savedConfig.id);
      
      set({
        currentConfiguration: updatedConfig,
        isLoading: false,
        error: undefined,
      });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Ошибка сохранения конфигурации',
      });
    }
  },

  addAccessoriesToConfiguration: async (accessories: Array<{component: Component, quantity: number}>) => {
    const state = get();
    
    if (!state.currentConfiguration?.id || state.currentConfiguration.id === '0') {
      set({ error: 'Сначала необходимо сохранить конфигурацию' });
      return;
    }

    set({ isLoading: true });

    try {
      for (const { component, quantity } of accessories) {
        await configurationsApi.addAccessory(state.currentConfiguration.id, component.id, quantity);
      }

      // Получаем обновленную конфигурацию
      const updatedConfig = await configurationsApi.getById(state.currentConfiguration.id);
      
      set({
        currentConfiguration: updatedConfig,
        isLoading: false,
        error: undefined,
      });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Ошибка добавления аксессуаров',
      });
    }
  },

  exportToPdf: async () => {
    const state = get();
    
    if (!state.currentConfiguration?.id || state.currentConfiguration.id === '0') {
      set({ error: 'Сначала необходимо сохранить конфигурацию' });
      return null;
    }

    set({ isLoading: true });

    try {
      const pdfBlob = await configurationsApi.exportToPdf(state.currentConfiguration.id);
      
      set({
        isLoading: false,
        error: undefined,
      });

      return pdfBlob;
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Ошибка экспорта в PDF',
      });
      return null;
    }
  },

  setLoading: (loading: boolean) => {
    set({ isLoading: loading });
  },

  setError: (error: string | null) => {
    set({ error: error || undefined });
  },
})); 