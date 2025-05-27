import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { motion } from 'framer-motion';
import { Search, Filter, X, Check, AlertCircle, Package } from 'lucide-react';
import { Component, ComponentFilter } from '../../types';
import { componentsApi, formatPrice, formatStock } from '../../lib/api';

interface ComponentSelectorProps {
  category: string;
  selectedComponent?: Component;
  onComponentSelect: (component: Component) => void;
  onComponentRemove: () => void;
}

export default function ComponentSelector({
  category,
  selectedComponent,
  onComponentSelect,
  onComponentRemove,
}: ComponentSelectorProps) {
  const [filters, setFilters] = useState<ComponentFilter>({
    category_slug: category,
    only_in_stock: false,
    page: 1,
    limit: 20,
  });
  
  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  // Загрузка компонентов
  const {
    data: componentsData,
    isLoading,
    error,
    refetch,
  } = useQuery(
    ['components', category, filters],
    () => componentsApi.getByCategory(category, filters),
    {
      enabled: !!category,
      keepPreviousData: true,
    }
  );

  // Обновление фильтров при смене категории
  useEffect(() => {
    setFilters(prev => ({
      ...prev,
      category_slug: category,
      page: 1,
    }));
    setSearchTerm('');
  }, [category]);

  // Обновление поискового запроса
  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      setFilters(prev => ({
        ...prev,
        search: searchTerm || undefined,
        page: 1,
      }));
    }, 500);

    return () => clearTimeout(debounceTimer);
  }, [searchTerm]);

  const handleFilterChange = (key: keyof ComponentFilter, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
      page: 1,
    }));
  };

  const getCategoryName = (slug: string) => {
    const names: Record<string, string> = {
      cpu: 'Процессоры',
      motherboard: 'Материнские платы',
      ram: 'Оперативная память',
      gpu: 'Видеокарты',
      storage: 'Накопители',
      psu: 'Блоки питания',
      case: 'Корпуса',
      cooler: 'Охлаждение',
    };
    return names[slug] || 'Компоненты';
  };

  const getStockColor = (status: string) => {
    switch (status) {
      case 'in_stock':
        return 'text-green-600 bg-green-50';
      case 'expected':
        return 'text-yellow-600 bg-yellow-50';
      case 'out_of_stock':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 h-full flex items-center justify-center">
        <div className="text-center">
          <div className="loading-dots mb-4">
            <div className="loading-dot"></div>
            <div className="loading-dot"></div>
            <div className="loading-dot"></div>
          </div>
          <p className="text-gray-600">Загрузка компонентов...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 h-full flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-4">Ошибка загрузки компонентов</p>
          <button onClick={() => refetch()} className="btn-primary">
            Попробовать снова
          </button>
        </div>
      </div>
    );
  }

  const components = componentsData || [];

  return (
    <div className="h-full flex flex-col">
      {/* Заголовок */}
      <div className="p-4 border-b bg-gray-50">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {getCategoryName(category)}
            </h3>
            {!isLoading && (
              <p className="text-sm text-gray-500">
                Найдено: {components.length} компонентов
              </p>
            )}
          </div>
          {selectedComponent && (
            <button
              onClick={onComponentRemove}
              className="text-red-600 hover:text-red-700 flex items-center space-x-1"
            >
              <X className="w-4 h-4" />
              <span className="text-sm">Убрать</span>
            </button>
          )}
        </div>

        {/* Поиск */}
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Поиск компонентов..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input pl-10 pr-10 w-full"
          />
          {isLoading && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            </div>
          )}
        </div>

        {/* Фильтры */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="btn-outline flex items-center space-x-2"
          >
            <Filter className="w-4 h-4" />
            <span>Фильтры</span>
          </button>

          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={filters.only_in_stock || false}
              onChange={(e) => handleFilterChange('only_in_stock', e.target.checked)}
              className="rounded border-gray-300"
            />
            <span className="text-sm text-gray-600">Только в наличии</span>
          </label>
        </div>

        {/* Расширенные фильтры */}
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 p-4 bg-white rounded-lg border"
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Цена от
                </label>
                <input
                  type="number"
                  placeholder="0"
                  value={filters.price_min || ''}
                  onChange={(e) => handleFilterChange('price_min', parseInt(e.target.value) || undefined)}
                  className="input w-full"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Цена до
                </label>
                <input
                  type="number"
                  placeholder="100000"
                  value={filters.price_max || ''}
                  onChange={(e) => handleFilterChange('price_max', parseInt(e.target.value) || undefined)}
                  className="input w-full"
                />
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Выбранный компонент */}
      {selectedComponent && (
        <div className="p-4 bg-blue-50 border-b">
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <Check className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1">
              <h4 className="font-medium text-gray-900">{selectedComponent.name}</h4>
              <p className="text-sm text-gray-600">{selectedComponent.brand}</p>
              <p className="text-sm font-medium text-green-600">
                {formatPrice(selectedComponent.price)}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Список компонентов */}
      <div className="flex-1 overflow-y-auto custom-scrollbar" style={{ maxHeight: 'calc(100vh - 400px)', minHeight: '300px' }}>
        {components.length === 0 ? (
          <div className="p-8 text-center">
            <Package className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">Компоненты не найдены</p>
            <p className="text-sm text-gray-500 mt-2">
              Попробуйте изменить фильтры или поисковый запрос
            </p>
          </div>
        ) : (
          <div className="p-4 space-y-3">
            {components.map((component) => (
              <motion.div
                key={component.id}
                className={`component-card ${
                  selectedComponent?.id === component.id ? 'selected' : ''
                } ${component.stock?.status === 'out_of_stock' ? 'unavailable' : ''}`}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => {
                  if (component.stock?.status !== 'out_of_stock') {
                    onComponentSelect(component);
                  }
                }}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-1">
                      {component.name}
                    </h4>
                    <p className="text-sm text-gray-600 mb-2">
                      {component.brand} • {component.model}
                    </p>
                    
                    {/* Основные характеристики */}
                    {component.specifications && (
                      <div className="text-xs text-gray-500 mb-2">
                        {Object.entries(component.specifications)
                          .slice(0, 2)
                          .map(([key, value]) => (
                            <span key={key} className="mr-2">
                              {key}: {value}
                            </span>
                          ))}
                      </div>
                    )}

                    {/* Цена */}
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-bold text-gray-900">
                        {formatPrice(component.price)}
                      </span>
                      
                      {/* Статус наличия */}
                      {component.stock && (
                        <span className={`px-2 py-1 text-xs rounded-full ${getStockColor(component.stock.status)}`}>
                          {formatStock(component.stock)}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Изображение */}
                  {component.image_url && (
                    <div className="ml-4 w-16 h-16 bg-gray-100 rounded-lg overflow-hidden">
                      <img
                        src={component.image_url}
                        alt={component.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )}
                </div>

                {/* Индикатор выбранного */}
                {selectedComponent?.id === component.id && (
                  <div className="absolute top-2 right-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <Check className="w-4 h-4 text-white" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
} 