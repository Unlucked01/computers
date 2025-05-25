import axios from 'axios';
import {
  Component,
  ComponentFilter,
  Configuration,
  CompatibilityCheck,
  ApiResponse,
  PaginatedResponse,
  ComponentCategory
} from '../types';

// Базовая конфигурация API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Добавляем отладку для проверки URL
console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptors для обработки ошибок
api.interceptors.request.use((config) => {
  console.log('API Request:', config.method?.toUpperCase(), config.url);
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    console.error('Request URL:', error.config?.url);
    console.error('Base URL:', error.config?.baseURL);
    return Promise.reject(error);
  }
);

// API для работы с категориями
export const categoriesApi = {
  getAll: async (): Promise<ComponentCategory[]> => {
    const response = await api.get<ComponentCategory[]>('/categories');
    return response.data;
  },
};

// API для работы с компонентами
export const componentsApi = {
  getAll: async (filters?: ComponentFilter): Promise<Component[]> => {
    const response = await api.get<Component[]>('/components', {
      params: filters,
    });
    return response.data;
  },

  getById: async (id: string): Promise<Component> => {
    const response = await api.get<Component>(`/components/${id}`);
    return response.data;
  },

  getByCategory: async (categorySlug: string, filters?: ComponentFilter): Promise<Component[]> => {
    // Убираем category_slug из параметров, так как он уже в URL
    const { category_slug, ...cleanFilters } = filters || {};
    
    const response = await api.get<Component[]>(`/components/category/${categorySlug}`, {
      params: cleanFilters,
    });
    return response.data;
  },
};

// API для проверки совместимости
export const checkCompatibilityAPI = async (componentIds: string[]): Promise<CompatibilityCheck> => {
  console.log('Checking compatibility for component IDs:', componentIds);
  console.log('Sending payload:', componentIds);
  
  const response = await api.post<CompatibilityCheck>('/components/check-compatibility', componentIds);
  return response.data;
};

// API для работы с конфигурациями
export const configurationsApi = {
  create: async (configuration: { name: string; description?: string }): Promise<Configuration> => {
    const response = await api.post<Configuration>('/configurations', configuration);
    return response.data;
  },

  addComponent: async (configId: string, componentId: string, quantity: number = 1, notes?: string): Promise<void> => {
    await api.post(`/configurations/${configId}/items`, {
      component_id: componentId,
      quantity,
      notes,
    });
  },

  checkCompatibility: async (configId: string): Promise<CompatibilityCheck> => {
    const response = await api.post<CompatibilityCheck>(`/configurations/${configId}/check-compatibility`);
    return response.data;
  },

  getById: async (id: string): Promise<Configuration> => {
    const response = await api.get<Configuration>(`/configurations/${id}`);
    return response.data;
  },

  getByUuid: async (uuid: string): Promise<Configuration> => {
    const response = await api.get<Configuration>(`/configurations/uuid/${uuid}`);
    return response.data;
  },

  exportToPdf: async (configurationId: string): Promise<Blob> => {
    const response = await api.get(`/configurations/${configurationId}/export/pdf`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

// Экспорт для обратной совместимости
export const createConfigurationAPI = configurationsApi.create;

// API для фильтров
export const filtersApi = {
  getFilterOptions: async (categorySlug?: string): Promise<any> => {
    const response = await api.get('/components/filters/options', {
      params: { category_slug: categorySlug },
    });
    return response.data;
  },
};

// Утилиты для работы с ошибками
export const handleApiError = (error: any): string => {
  if (error.response?.data?.error) {
    return error.response.data.error;
  }
  if (error.message) {
    return error.message;
  }
  return 'Произошла неизвестная ошибка';
};

// Хелперы для форматирования данных
export const formatPrice = (price: number, currency: string = 'RUB'): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
  }).format(price);
};

export const formatStock = (stock: any): string => {
  switch (stock?.status) {
    case 'in_stock':
      return `В наличии (${stock.quantity})`;
    case 'expected':
      return `Ожидается ${stock.expected_date ? new Date(stock.expected_date).toLocaleDateString('ru-RU') : ''}`;
    case 'out_of_stock':
      return 'Нет в наличии';
    default:
      return 'Статус неизвестен';
  }
};

export default api; 