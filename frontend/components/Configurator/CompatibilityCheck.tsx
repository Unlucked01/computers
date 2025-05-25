import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, XCircle, Info, Zap } from 'lucide-react';
import { Configuration, CompatibilityIssue } from '../../types';

interface CompatibilityCheckProps {
  configuration?: Configuration;
}

export default function CompatibilityCheck({ configuration }: CompatibilityCheckProps) {
  if (!configuration || !configuration.items || configuration.items.length < 2) {
    return (
      <div className="text-center py-8">
        <Info className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">
          Добавьте компоненты для проверки совместимости
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Минимум 2 компонента для анализа
        </p>
      </div>
    );
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'compatible':
        return <CheckCircle className="w-6 h-6 text-green-500" />;
      case 'warning':
        return <AlertTriangle className="w-6 h-6 text-yellow-500" />;
      case 'incompatible':
        return <XCircle className="w-6 h-6 text-red-500" />;
      default:
        return <Info className="w-6 h-6 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'compatible':
        return 'bg-green-50 border-green-200 text-green-700';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 text-yellow-700';
      case 'incompatible':
        return 'bg-red-50 border-red-200 text-red-700';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-700';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'compatible':
        return 'Все компоненты совместимы';
      case 'warning':
        return 'Есть предупреждения';
      case 'incompatible':
        return 'Обнаружены проблемы';
      default:
        return 'Проверка совместимости';
    }
  };

  const getIssueSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 'info':
        return <Info className="w-5 h-5 text-blue-500" />;
      default:
        return <Info className="w-5 h-5 text-gray-500" />;
    }
  };

  const issues = configuration.compatibility_issues || [];

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Проверка совместимости
      </h3>

      {/* Общий статус */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={`p-4 rounded-lg border ${getStatusColor(configuration.compatibility_status)}`}
      >
        <div className="flex items-center space-x-3">
          {getStatusIcon(configuration.compatibility_status)}
          <div className="flex-1">
            <h4 className="font-medium">
              {getStatusText(configuration.compatibility_status)}
            </h4>
            <p className="text-sm opacity-75">
              Проверено {configuration.items.length} компонентов
            </p>
          </div>
        </div>
      </motion.div>

      {/* Энергопотребление */}
      {configuration.compatibility_issues?.some(issue => issue.type === 'power') && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center space-x-2 mb-2">
            <Zap className="w-5 h-5 text-blue-600" />
            <span className="font-medium text-blue-700">Энергопотребление</span>
          </div>
          <div className="text-sm text-blue-600">
            {/* Здесь можно добавить расчет общего энергопотребления */}
            <p>Рекомендуемая мощность БП: {configuration.compatibility_issues.find(i => i.type === 'power')?.suggestions?.[0] || 'Проверьте характеристики'}</p>
          </div>
        </div>
      )}

      {/* Список проблем */}
      {issues.length > 0 && (
        <div className="space-y-3">
          <h4 className="font-medium text-gray-900">Обнаруженные проблемы:</h4>
          {issues.map((issue, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-3 bg-white border rounded-lg"
            >
              <div className="flex items-start space-x-3">
                {getIssueSeverityIcon(issue.severity)}
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">
                    {issue.message}
                  </p>
                  {issue.suggestions && issue.suggestions.length > 0 && (
                    <div className="mt-2">
                      <p className="text-xs text-gray-600 mb-1">Рекомендации:</p>
                      <ul className="text-xs text-gray-600 space-y-1">
                        {issue.suggestions.map((suggestion, suggestionIndex) => (
                          <li key={suggestionIndex} className="flex items-start space-x-1">
                            <span>•</span>
                            <span>{suggestion}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Если нет проблем */}
      {issues.length === 0 && configuration.compatibility_status === 'compatible' && (
        <div className="text-center py-4">
          <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-2" />
          <p className="text-green-700 font-medium">
            Отлично! Все компоненты совместимы
          </p>
          <p className="text-sm text-green-600 mt-1">
            Ваша конфигурация готова к сборке
          </p>
        </div>
      )}

      {/* Дополнительная информация */}
      <div className="mt-6 p-3 bg-gray-50 rounded-lg">
        <h5 className="text-sm font-medium text-gray-700 mb-2">
          Что проверяется:
        </h5>
        <ul className="text-xs text-gray-600 space-y-1">
          <li>• Совместимость сокета процессора и материнской платы</li>
          <li>• Тип и частота оперативной памяти</li>
          <li>• Энергопотребление и мощность блока питания</li>
          <li>• Форм-фактор корпуса и материнской платы</li>
          <li>• Интерфейсы подключения накопителей</li>
        </ul>
      </div>
    </div>
  );
} 