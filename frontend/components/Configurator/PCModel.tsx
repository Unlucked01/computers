import React from 'react';
import { motion } from 'framer-motion';
import { X, Maximize2, Cpu, HardDrive, Zap, Fan, MemoryStick, Monitor, Boxes } from 'lucide-react';
import { Component } from '../../types';

interface PCModelProps {
  selectedComponents: Record<string, Component>;
  selectedCategory: string;
  onComponentClick: (category: string) => void;
  expanded: boolean;
  onClose: () => void;
}

interface ComponentPosition {
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
  category: string;
  icon: React.ReactNode;
  depth?: number;
  shape?: 'motherboard' | 'cpu' | 'ram' | 'gpu' | 'storage' | 'psu' | 'cooler';
}

export default function PCModel({
  selectedComponents,
  selectedCategory,
  onComponentClick,
  expanded,
  onClose,
}: PCModelProps) {
  // Позиции компонентов в 3D модели ПК (в процентах) - схематичное расположение
  const componentPositions: ComponentPosition[] = [
    { 
      x: 10, y: 25, width: 65, height: 50, 
      label: 'Материнская плата', category: 'motherboard', 
      icon: <Boxes className="w-6 h-6" />,
      depth: 1,
      shape: 'motherboard'
    },
    { 
      x: 15, y: 30, width: 15, height: 15, 
      label: 'CPU', category: 'cpu', 
      icon: <Cpu className="w-5 h-5" />,
      depth: 2,
      shape: 'cpu'
    },
    { 
      x: 40, y: 28, width: 4, height: 22, 
      label: 'RAM', category: 'ram', 
      icon: <MemoryStick className="w-4 h-4" />,
      depth: 3,
      shape: 'ram'
    },
    { 
      x: 46, y: 28, width: 4, height: 22, 
      label: 'RAM', category: 'ram', 
      icon: <MemoryStick className="w-4 h-4" />,
      depth: 3,
      shape: 'ram'
    },
    { 
      x: 12, y: 52, width: 45, height: 20, 
      label: 'GPU', category: 'gpu', 
      icon: <Monitor className="w-6 h-6" />,
      depth: 4,
      shape: 'gpu'
    },
    { 
      x: 78, y: 35, width: 15, height: 8, 
      label: 'SSD', category: 'storage', 
      icon: <HardDrive className="w-4 h-4" />,
      depth: 2,
      shape: 'storage'
    },
    { 
      x: 78, y: 70, width: 18, height: 18, 
      label: 'PSU', category: 'psu', 
      icon: <Zap className="w-5 h-5" />,
      depth: 1,
      shape: 'psu'
    },
    { 
      x: 35, y: 10, width: 12, height: 12, 
      label: 'Охлаждение', category: 'cooler', 
      icon: <Fan className="w-5 h-5" />,
      depth: 6,
      shape: 'cooler'
    },
  ];

  const [hoveredComponent, setHoveredComponent] = React.useState<string | null>(null);

  const getComponentStatus = (category: string) => {
    if (selectedComponents[category]) {
      return 'selected';
    }
    if (selectedCategory === category) {
      return 'highlighted';
    }
    return 'default';
  };

  // Проверяем, находится ли компонент на материнской плате
  const isOnMotherboard = (category: string) => {
    return ['cpu', 'ram', 'gpu', 'cooler'].includes(category);
  };

  // Определяем, можно ли кликнуть на компонент
  const isClickable = (category: string) => {
    // Все компоненты всегда кликабельны
    return true;
  };

  // Определяем, можно ли применить hover эффект
  const isHoverable = (category: string) => {
    // Материнская плата не увеличивается при наведении
    if (category === 'motherboard') {
      return false;
    }
    return isClickable(category);
  };

  const getSchematicStyle = (shape: string, status: string, depth: number = 1) => {
    const baseStyles = {
      borderWidth: '2px',
      borderStyle: 'solid',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    } as React.CSSProperties;

    const statusStyles = {
      selected: {
        borderColor: '#22c55e',
        boxShadow: '0 0 20px rgba(34, 197, 94, 0.4), inset 0 1px 3px rgba(255,255,255,0.1)',
      },
      highlighted: {
        borderColor: '#3b82f6',
        boxShadow: '0 0 20px rgba(59, 130, 246, 0.4), inset 0 1px 3px rgba(255,255,255,0.1)',
        transform: 'scale(1.05)',
      },
      default: {
        borderColor: '#64748b',
        boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.2)',
      }
    };

    const shapeStyles = {
      motherboard: {
        background: 'linear-gradient(145deg, #1e293b, #334155)',
        borderRadius: '8px',
      },
      cpu: {
        background: 'linear-gradient(145deg, #374151, #4b5563)',
        borderRadius: '4px',
      },
      ram: {
        background: 'linear-gradient(145deg, #059669, #047857)',
        borderRadius: '2px',
      },
      gpu: {
        background: 'linear-gradient(145deg, #7c2d12, #9a3412)',
        borderRadius: '6px',
      },
      storage: {
        background: 'linear-gradient(145deg, #1f2937, #374151)',
        borderRadius: '3px',
      },
      psu: {
        background: 'linear-gradient(145deg, #18181b, #27272a)',
        borderRadius: '6px',
      },
      cooler: {
        background: 'radial-gradient(circle, #6366f1, #4f46e5)',
        borderRadius: '50%',
      }
    };

    return {
      ...baseStyles,
      ...shapeStyles[shape as keyof typeof shapeStyles],
      ...statusStyles[status as keyof typeof statusStyles],
      transform: `translateZ(${depth * 2}px) ${status === 'highlighted' ? 'scale(1.05)' : 'scale(1)'}`,
    } as React.CSSProperties;
  };

  const renderComponentDetails = (position: ComponentPosition) => {
    const { shape } = position;
    
    switch (shape) {
      case 'motherboard':
        return (
          <div className="absolute inset-0 pointer-events-none">
            {/* Слоты и разъемы на материнской плате */}
            <div className="absolute top-2 left-2 w-4 h-1 bg-yellow-500 rounded opacity-60"></div>
            <div className="absolute top-4 left-2 w-4 h-1 bg-yellow-500 rounded opacity-60"></div>
            <div className="absolute bottom-2 right-2 w-3 h-3 bg-blue-500 rounded opacity-60"></div>
            <div className="absolute bottom-2 left-8 w-8 h-1 bg-gray-400 rounded opacity-60"></div>
            {/* Чипсет */}
            <div className="absolute bottom-4 left-4 w-6 h-6 bg-gray-600 rounded border border-gray-500"></div>
          </div>
        );
      case 'cpu':
        return (
          <div className="absolute inset-0 pointer-events-none">
            {/* Контакты процессора */}
            <div className="absolute inset-1 grid grid-cols-6 gap-0.5 opacity-40">
              {Array.from({ length: 36 }).map((_, i) => (
                <div key={i} className="w-0.5 h-0.5 bg-yellow-400 rounded-full"></div>
              ))}
            </div>
            {/* Крышка процессора */}
            <div className="absolute inset-2 bg-gray-500 rounded border border-gray-400 opacity-80"></div>
          </div>
        );
      case 'ram':
        return (
          <div className="absolute inset-0 pointer-events-none">
            {/* Чипы памяти */}
            <div className="absolute top-1 left-0.5 right-0.5 h-1 bg-black rounded opacity-60"></div>
            <div className="absolute top-3 left-0.5 right-0.5 h-1 bg-black rounded opacity-60"></div>
            <div className="absolute bottom-3 left-0.5 right-0.5 h-1 bg-black rounded opacity-60"></div>
            <div className="absolute bottom-1 left-0.5 right-0.5 h-1 bg-black rounded opacity-60"></div>
            {/* Разъем */}
            <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-yellow-500"></div>
          </div>
        );
      case 'gpu':
        return (
          <div className="absolute inset-0 pointer-events-none">
            {/* Кулеры видеокарты */}
            <div className="absolute top-2 left-4 w-6 h-6 border-2 border-gray-400 rounded-full opacity-60">
              <div className="absolute inset-1 border border-gray-400 rounded-full"></div>
            </div>
            <div className="absolute top-2 right-8 w-6 h-6 border-2 border-gray-400 rounded-full opacity-60">
              <div className="absolute inset-1 border border-gray-400 rounded-full"></div>
            </div>
            {/* Разъемы питания */}
            <div className="absolute top-1 right-2 w-2 h-3 bg-yellow-500 rounded opacity-80"></div>
            {/* Выходы */}
            <div className="absolute bottom-1 right-1 w-6 h-2 bg-blue-600 rounded opacity-80"></div>
          </div>
        );
      case 'storage':
        return (
          <div className="absolute inset-0 pointer-events-none">
            {/* Разъем SATA */}
            <div className="absolute bottom-0 left-1 w-4 h-1 bg-red-500 rounded opacity-80"></div>
            {/* Контроллер */}
            <div className="absolute top-1 left-1 right-1 h-2 bg-gray-600 rounded opacity-60"></div>
          </div>
        );
      case 'psu':
        return (
          <div className="absolute inset-0 pointer-events-none">
            {/* Вентилятор БП */}
            <div className="absolute inset-2 border-2 border-gray-500 rounded-full opacity-60">
              <div className="absolute inset-1 border border-gray-500 rounded-full"></div>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-gray-600 rounded-full"></div>
            </div>
            {/* Кабели */}
            <div className="absolute top-0 left-2 w-1 h-2 bg-red-500 rounded opacity-80"></div>
            <div className="absolute top-0 left-4 w-1 h-2 bg-yellow-500 rounded opacity-80"></div>
          </div>
        );
      case 'cooler':
        return (
          <div className="absolute inset-0 pointer-events-none">
            {/* Лопасти кулера */}
            <div className="absolute inset-1 border-2 border-white rounded-full opacity-60">
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-white rounded-full"></div>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rotate-45">
                <div className="w-0.5 h-4 bg-white opacity-80"></div>
                <div className="w-4 h-0.5 bg-white opacity-80 -mt-2"></div>
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  const getTotalPrice = () => {
    return Object.values(selectedComponents).reduce((sum, component) => sum + component.price, 0);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className={`relative w-full h-full ${expanded ? 'bg-gray-50' : ''}`}>
      {expanded && (
        <div className="absolute top-4 right-4 z-10">
          <button
            onClick={onClose}
            className="p-2 bg-white rounded-full shadow-lg hover:bg-gray-50 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
      )}

      <div className="w-full h-full flex items-start justify-center p-6">
        <div className="relative w-full max-w-4xl aspect-[16/10]">
          {/* Основной корпус компьютера */}
          <div className="relative w-full h-full bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-3xl shadow-2xl border border-gray-700 overflow-hidden"
               style={{ 
                 background: 'linear-gradient(145deg, #1f2937, #111827)',
                 boxShadow: 'inset 0 2px 4px rgba(255,255,255,0.1), 0 25px 50px -12px rgba(0,0,0,0.25)'
               }}>
            
            {/* Боковые панели для создания 3D эффекта */}
            <div className="absolute inset-0 rounded-3xl" style={{
              background: 'linear-gradient(90deg, rgba(0,0,0,0.3) 0%, transparent 10%, transparent 90%, rgba(0,0,0,0.2) 100%)'
            }}></div>
            
            {/* Передняя панель с вентиляционными отверстиями */}
            <div className="absolute left-4 top-6 bottom-6 w-3 bg-gradient-to-b from-gray-600 to-gray-800 rounded-lg shadow-inner"></div>
            
            {/* Световая полоса RGB */}
            <motion.div
              className="absolute bottom-4 left-8 right-8 h-2 rounded-full opacity-80"
              style={{
                background: 'linear-gradient(90deg, #ff0080, #ff8000, #00ff80, #0080ff, #8000ff, #ff0080)',
                backgroundSize: '300% 100%'
              }}
              animate={{
                backgroundPosition: ['0% 50%', '100% 50%']
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: 'linear'
              }}
            />
            
            {/* Вентиляционная решетка */}
            <div className="absolute top-6 right-6 grid grid-cols-6 gap-1 opacity-60">
              {Array.from({ length: 24 }).map((_, i) => (
                <div key={i} className="w-1.5 h-1.5 bg-gray-500 rounded-full shadow-inner"></div>
              ))}
            </div>

            {/* Схематичные компоненты */}
            <div className="absolute inset-0 perspective-1000">
              {componentPositions.map((position, index) => {
                const status = getComponentStatus(position.category);
                const component = selectedComponents[position.category];
                const componentStyle = getSchematicStyle(position.shape || 'motherboard', status, position.depth);
                const clickable = isClickable(position.category);
                const hoverable = isHoverable(position.category);

                return (
                  <motion.div
                    key={`${position.category}-${index}`}
                    className="absolute"
                    style={{
                      left: `${position.x}%`,
                      top: `${position.y}%`,
                      width: `${position.width}%`,
                      height: `${position.height}%`,
                      ...componentStyle,
                      pointerEvents: clickable ? 'auto' : 'none',
                      zIndex: position.depth,
                    }}
                    whileHover={hoverable ? { 
                      scale: 1.1,
                      zIndex: 20,
                      transition: { duration: 0.2 }
                    } : {}}
                    whileTap={clickable ? { scale: 0.95 } : {}}
                    onClick={clickable ? () => onComponentClick(position.category) : undefined}
                    onMouseEnter={() => setHoveredComponent(position.category)}
                    onMouseLeave={() => setHoveredComponent(null)}
                    animate={status === 'highlighted' ? { 
                      scale: [1, 1.05, 1],
                      transition: { duration: 1, repeat: Infinity }
                    } : {}}
                  >
                    {/* Схематичные детали компонента */}
                    {renderComponentDetails(position)}

                    {/* Иконка и название компонента - адаптивные размеры */}
                    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white text-center pointer-events-none z-10">
                      <div className="flex flex-col items-center justify-center">
                        <div className={`mb-0.5 opacity-90 drop-shadow-lg ${
                          expanded ? 'text-base' : 'text-xs'
                        }`}>
                          {React.cloneElement(position.icon as React.ReactElement, {
                            className: expanded ? 'w-6 h-6' : position.width < 10 ? 'w-3 h-3' : 'w-4 h-4'
                          })}
                        </div>
                        <span className={`font-semibold leading-tight drop-shadow-lg ${
                          expanded ? 'text-sm' : position.width < 10 ? 'text-[8px]' : 'text-xs'
                        }`}>
                          {expanded ? position.label : position.label.length > 8 ? 
                            position.label.substring(0, 6) + '...' : position.label}
                        </span>
                      </div>
                    </div>

                    {/* Индикатор выбранного компонента */}
                    {component && (
                      <>
                        <motion.div
                          className={`absolute -top-1 -right-1 bg-green-400 rounded-full border-2 border-white shadow-lg z-20 ${
                            expanded ? 'w-4 h-4' : 'w-3 h-3'
                          }`}
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{ duration: 2, repeat: Infinity }}
                        />
                        <div className="absolute inset-0 rounded border-2 border-green-300 animate-pulse z-15"></div>
                      </>
                    )}

                    {/* Информация о компоненте при наведении */}
                    {component && clickable && expanded && (
                      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-black/90 text-white text-xs rounded-lg shadow-lg opacity-0 hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-30">
                        <div className="font-medium">{component.name}</div>
                        <div className="text-gray-300">{formatPrice(component.price)}</div>
                        <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-black/90"></div>
                      </div>
                    )}

                    {/* Подсветка при наведении на пустые слоты */}
                    {!component && status === 'highlighted' && clickable && (
                      <div className="absolute inset-0 rounded border-2 border-blue-400 animate-pulse z-15"></div>
                    )}

                    {/* Затемнение некликабельных компонентов */}
                    {!clickable && (
                      <div className="absolute inset-0 bg-black/30 rounded z-15 pointer-events-none"></div>
                    )}
                  </motion.div>
                );
              })}
            </div>

            {/* Эффект питания */}
            {Object.keys(selectedComponents).length > 0 && (
              <>
                {/* Пульсирующий свет */}
                <motion.div
                  className="absolute inset-0 pointer-events-none rounded-3xl"
                  animate={{ 
                    boxShadow: [
                      '0 0 20px rgba(59, 130, 246, 0.1)',
                      '0 0 40px rgba(59, 130, 246, 0.2)',
                      '0 0 20px rgba(59, 130, 246, 0.1)'
                    ]
                  }}
                  transition={{ duration: 3, repeat: Infinity }}
                />
                
                {/* LED индикатор питания */}
                <motion.div
                  className="absolute top-6 left-6 w-3 h-3 bg-green-400 rounded-full shadow-lg"
                  animate={{ opacity: [0.5, 1, 0.5] }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
              </>
            )}
          </div>

          {/* Подсказка для текущего компонента */}
          {!expanded && (
            <div className="absolute -top-12 left-0 right-0 text-center">
              <p className="text-sm text-gray-600 bg-white px-4 py-2 rounded-lg shadow-sm inline-block">
                {selectedComponents[selectedCategory] 
                  ? `✓ ${selectedComponents[selectedCategory].name}`
                  : `Выберите ${getCategoryDisplayName(selectedCategory)}`
                }
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Информационная панель - перенесена ниже */}
      <div className="p-4 mb-4 bg-white rounded-2xl shadow-xl border p-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="text-sm">
              <span className="text-gray-600">Компонентов:</span>
              <span className="font-bold text-gray-900 ml-2">
                {Object.keys(selectedComponents).length}/7
              </span>
            </div>
            <div className="w-px h-6 bg-gray-300"></div>
            <div className="text-sm">
              <span className="text-gray-600">Общая стоимость:</span>
              <span className="font-bold text-green-600 ml-2">
                {formatPrice(getTotalPrice())}
              </span>
            </div>
          </div>
          
          {/* Индикаторы статуса */}
          <div className="flex items-center space-x-2">
            <div className={`flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium ${
              Object.keys(selectedComponents).length >= 5 
                ? 'bg-green-100 text-green-800' 
                : 'bg-yellow-100 text-yellow-800'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                Object.keys(selectedComponents).length >= 5 ? 'bg-green-400' : 'bg-yellow-400'
              }`}></div>
              {Object.keys(selectedComponents).length >= 5 ? 'Готов к сборке' : 'Требуются компоненты'}
            </div>
          </div>
        </div>

        {/* Прогресс-бар */}
        <div className="mt-3 w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-blue-400 to-green-400 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${(Object.keys(selectedComponents).length / 7) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>
    </div>
  );
}

function getCategoryDisplayName(category: string): string {
  const names: Record<string, string> = {
    cpu: 'процессор',
    motherboard: 'материнскую плату',
    ram: 'оперативную память',
    gpu: 'видеокарту',
    storage: 'накопитель',
    psu: 'блок питания',
    cooler: 'охлаждение',
    case: 'корпус'
  };
  return names[category] || 'компонент';
} 