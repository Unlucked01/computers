import React, { useState } from 'react';
import { motion } from 'framer-motion';
import PCModel from './PCModel';
import ComponentSelector from './ComponentSelector';
import ConfigSummary from './ConfigSummary';
import CompatibilityCheck from './CompatibilityCheck';
import { useConfiguratorStore } from '../../hooks/useConfiguratorStore';
import { Component, ComponentCategory } from '../../types';

export default function Configurator() {
  const [selectedCategory, setSelectedCategory] = useState<string>('cpu');
  const [isModelExpanded, setIsModelExpanded] = useState(false);
  
  const {
    selectedComponents,
    currentConfiguration: configuration,
    addComponent,
    removeComponent,
    checkCompatibility,
    isLoading,
    error
  } = useConfiguratorStore();

  const categories: ComponentCategory[] = [
    { id: "1", name: 'Процессор', slug: 'cpu', order_priority: 1, icon: '🔲' },
    { id: "2", name: 'Материнская плата', slug: 'motherboard', order_priority: 2, icon: '🔧' },
    { id: "3", name: 'Оперативная память', slug: 'ram', order_priority: 3, icon: '💾' },
    { id: "4", name: 'Видеокарта', slug: 'gpu', order_priority: 4, icon: '🎮' },
    { id: "5", name: 'Накопитель', slug: 'storage', order_priority: 5, icon: '💿' },
    { id: "6", name: 'Блок питания', slug: 'psu', order_priority: 6, icon: '⚡' },
    { id: "7", name: 'Корпус', slug: 'case', order_priority: 7, icon: '📦' },
    { id: "8", name: 'Охлаждение', slug: 'cooler', order_priority: 8, icon: '❄️' },
  ];

  const handleComponentSelect = (component: Component) => {
    addComponent(component);
    checkCompatibility();
  };

  const handleComponentRemove = (categorySlug: string) => {
    removeComponent(categorySlug);
    checkCompatibility();
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
      {/* Заголовок конфигуратора */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
        <h2 className="text-2xl md:text-3xl font-bold mb-2">
          Конфигуратор ПК
        </h2>
        <p className="text-blue-100">
          Выберите компоненты для вашего идеального компьютера
        </p>
      </div>

      {/* Основной контент */}
      <div className="grid grid-cols-1 lg:grid-cols-12 min-h-[800px]">
        {/* Левая панель - Категории */}
        <div className="lg:col-span-3 bg-gray-50 border-r">
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Компоненты
            </h3>
            <div className="space-y-2">
              {categories.map((category) => (
                <button
                  key={category.slug}
                  onClick={() => setSelectedCategory(category.slug)}
                  className={`w-full text-left p-3 rounded-lg transition-colors duration-200 flex items-center space-x-3 ${
                    selectedCategory === category.slug
                      ? 'bg-blue-600 text-white'
                      : 'bg-white hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  <span className="text-lg">{category.icon}</span>
                  <div className="flex-1">
                    <span className="font-medium">{category.name}</span>
                    {selectedComponents[category.slug] && (
                      <div className="text-xs opacity-75 truncate">
                        {selectedComponents[category.slug].name}
                      </div>
                    )}
                  </div>
                  {selectedComponents[category.slug] && (
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  )}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Центральная часть - Модель ПК */}
        <div className="lg:col-span-5 relative">
          <div className="sticky top-20">
            <div className="p-6 h-full flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  Визуализация сборки
                </h3>
                <button
                  onClick={() => setIsModelExpanded(!isModelExpanded)}
                  className="btn-outline"
                >
                  {isModelExpanded ? 'Свернуть' : 'Развернуть'}
                </button>
              </div>

              <div className={`flex-1 bg-gradient-to-br from-slate-100 to-slate-200 rounded-xl ${
                isModelExpanded ? 'fixed inset-0 z-50 p-8' : ''
              }`}>
                <PCModel
                  selectedComponents={selectedComponents}
                  selectedCategory={selectedCategory}
                  onComponentClick={setSelectedCategory}
                  expanded={isModelExpanded}
                  onClose={() => setIsModelExpanded(false)}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Правая панель - Селектор компонентов */}
        <div className="lg:col-span-4 border-l">
          <div className="h-full flex flex-col">
            <ComponentSelector
              category={selectedCategory}
              selectedComponent={selectedComponents[selectedCategory]}
              onComponentSelect={handleComponentSelect}
              onComponentRemove={() => handleComponentRemove(selectedCategory)}
            />
          </div>
        </div>
      </div>

      {/* Нижняя панель - Сводка и совместимость */}
      <div className="border-t bg-gray-50">
        <div className="grid grid-cols-1 lg:grid-cols-2">
          <div className="p-6 border-r">
            <CompatibilityCheck configuration={configuration} />
          </div>
          <div className="p-6">
            <ConfigSummary
              selectedComponents={selectedComponents}
              configuration={configuration}
            />
          </div>
        </div>
      </div>

      {/* Ошибки */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-50 border-l-4 border-red-400 p-4 m-4"
        >
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
} 