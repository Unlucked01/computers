import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Save, ShoppingCart, Calculator, Package } from 'lucide-react';
import { Component, Configuration } from '../../types';
import { formatPrice } from '../../lib/api';
import { useConfiguratorStore } from '../../hooks/useConfiguratorStore';
import AccessorySelector from './AccessorySelector';
import { useRouter } from 'next/router';

interface ConfigSummaryProps {
  selectedComponents: Record<string, Component>;
  configuration?: Configuration;
}

export default function ConfigSummary({ selectedComponents, configuration }: ConfigSummaryProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [showAccessorySelector, setShowAccessorySelector] = useState(false);
  const [configName, setConfigName] = useState('');
  const [configDescription, setConfigDescription] = useState('');

  const { saveConfiguration, exportToPdf, addAccessoriesToConfiguration, isLoading } = useConfiguratorStore();
  const router = useRouter();

  const componentList = Object.values(selectedComponents);
  const totalPrice = componentList.reduce((sum, component) => sum + component.price, 0);
  const componentCount = componentList.length;

  const handleSave = async () => {
    if (!configName.trim()) return;
    
    try {
      await saveConfiguration(configName, configDescription);
      setShowSaveDialog(false);
      setConfigName('');
      setConfigDescription('');
    } catch (error) {
      console.error('Ошибка сохранения:', error);
    }
  };

  const handleExportPDF = async () => {
    if (!isConfigurationSaved) {
      return;
    }
    
    // Показываем селектор аксессуаров перед экспортом
    setShowAccessorySelector(true);
  };

  const handleAccessoriesSelected = async (selectedAccessories: Array<{component: Component, quantity: number}>) => {
    setIsExporting(true);
    try {
      // Добавляем выбранные аксессуары в конфигурацию
      if (selectedAccessories.length > 0) {
        await addAccessoriesToConfiguration(selectedAccessories);
      }
      
      // Экспортируем в PDF
      const pdfBlob = await exportToPdf();
      if (pdfBlob) {
        // Создаем ссылку для скачивания
        const url = window.URL.createObjectURL(pdfBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `конфигурация_${configuration?.name || 'config'}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Ошибка экспорта:', error);
    } finally {
      setIsExporting(false);
    }
  };



  const isConfigurationSaved = configuration?.id && configuration.id !== '0';

  console.log('ConfigSummary - configuration:', configuration);
  console.log('ConfigSummary - isConfigurationSaved:', isConfigurationSaved);

  const getCategoryName = (slug: string) => {
    const names: Record<string, string> = {
      cpu: 'Процессор',
      motherboard: 'Материнская плата',
      ram: 'Оперативная память',
      gpu: 'Видеокарта',
      storage: 'Накопитель',
      psu: 'Блок питания',
      case: 'Корпус',
      cooler: 'Охлаждение',
    };
    return names[slug] || 'Компонент';
  };

  if (componentCount === 0) {
    return (
      <div className="text-center py-8">
        <Package className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">
          Конфигурация пуста
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Добавьте компоненты для просмотра сводки
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <h3 className="text-lg font-semibold text-gray-900">
            Сводка конфигурации
          </h3>
          {isConfigurationSaved && (
            <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
              Сохранена
            </span>
          )}
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <Calculator className="w-4 h-4" />
          <span>{componentCount} компонентов</span>
        </div>
      </div>

      {/* Список выбранных компонентов */}
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {componentList.map((component) => (
          <motion.div
            key={component.id}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">
                {component.category.name}
              </p>
              <p className="text-xs text-gray-600 truncate">
                {component.brand} {component.name}
              </p>
            </div>
            <div className="text-sm font-medium text-gray-900">
              {formatPrice(component.price)}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Итоговая цена */}
      <div className="border-t pt-4">
        <div className="flex items-center justify-between">
          <span className="text-lg font-semibold text-gray-900">
            Итого:
          </span>
          <span className="text-2xl font-bold text-green-600">
            {formatPrice(totalPrice)}
          </span>
        </div>
        
        {/* Дополнительная информация */}
        <div className="mt-2 text-sm text-gray-600">
          <p>• Цены указаны без учета доставки</p>
          <p>• Наличие компонентов может изменяться</p>
        </div>
      </div>

      {/* Действия */}
      <div className="space-y-3 pt-4 border-t">
        {/* Сохранение конфигурации */}
        <button
          onClick={() => setShowSaveDialog(true)}
          disabled={componentCount === 0}
          className="btn-primary w-full flex items-center justify-center space-x-2"
        >
          <Save className="w-4 h-4" />
          <span>Сохранить конфигурацию</span>
        </button>

        {/* Дополнительные действия */}
        <div className="flex justify-center">
          <button
            onClick={handleExportPDF}
            disabled={!isConfigurationSaved || isExporting}
            className="btn-outline flex items-center justify-center space-x-2 w-full"
          >
            <Download className="w-4 h-4" />
            <span>{isExporting ? 'Экспорт...' : 'Экспорт в PDF'}</span>
          </button>
        </div>

        {/* Покупка (заглушка) */}
        <button
          onClick={() => router.push('/payment')}
          disabled={componentCount === 0}
          className="btn-secondary w-full flex items-center justify-center space-x-2"
        >
          <ShoppingCart className="w-4 h-4" />
          <span>Перейти к покупке</span>
        </button>
      </div>

      {/* Диалог сохранения */}
      {showSaveDialog && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          onClick={() => setShowSaveDialog(false)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white rounded-lg p-6 max-w-md w-full mx-4"
            onClick={(e) => e.stopPropagation()}
          >
            <h4 className="text-lg font-semibold text-gray-900 mb-4">
              Сохранить конфигурацию
            </h4>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Название конфигурации *
                </label>
                <input
                  type="text"
                  value={configName}
                  onChange={(e) => setConfigName(e.target.value)}
                  placeholder="Мой игровой ПК"
                  className="input w-full"
                  autoFocus
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Описание
                </label>
                <textarea
                  value={configDescription}
                  onChange={(e) => setConfigDescription(e.target.value)}
                  placeholder="Описание сборки (необязательно)"
                  className="input w-full h-20 resize-none"
                />
              </div>
            </div>

            <div className="flex space-x-3 mt-6">
              <button
                onClick={() => setShowSaveDialog(false)}
                className="btn-outline flex-1"
              >
                Отмена
              </button>
              <button
                onClick={handleSave}
                disabled={!configName.trim()}
                className="btn-primary flex-1"
              >
                Сохранить
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}

      {/* Селектор аксессуаров */}
      <AccessorySelector
        isOpen={showAccessorySelector}
        onClose={() => setShowAccessorySelector(false)}
        onConfirm={handleAccessoriesSelected}
      />
    </div>
  );
} 