import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Plus, Minus, ShoppingCart } from 'lucide-react';
import { Component } from '../../types';
import { formatPrice } from '../../lib/api';

interface AccessorySelectorProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (selectedAccessories: SelectedAccessory[]) => void;
}

interface SelectedAccessory {
  component: Component;
  quantity: number;
}

export default function AccessorySelector({ isOpen, onClose, onConfirm }: AccessorySelectorProps) {
  const [accessories, setAccessories] = useState<Component[]>([]);
  const [selectedAccessories, setSelectedAccessories] = useState<SelectedAccessory[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  useEffect(() => {
    if (isOpen) {
      loadAccessories();
    }
  }, [isOpen]);

  const loadAccessories = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/accessories?limit=50`);
      const data = await response.json();
      setAccessories(data);
    } catch (error) {
      console.error('Ошибка загрузки аксессуаров:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredAccessories = accessories.filter(accessory => {
    const matchesSearch = accessory.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         accessory.brand.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || 
                           accessory.specifications?.type === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = [
    { value: 'all', label: 'Все категории' },
    { value: 'mouse', label: 'Мыши' },
    { value: 'keyboard', label: 'Клавиатуры' },
    { value: 'monitor', label: 'Мониторы' },
    { value: 'headset', label: 'Гарнитуры' },
    { value: 'webcam', label: 'Веб-камеры' },
    { value: 'mousepad', label: 'Коврики' },
  ];

  const addAccessory = (accessory: Component) => {
    const existing = selectedAccessories.find(item => item.component.id === accessory.id);
    if (existing) {
      setSelectedAccessories(prev => 
        prev.map(item => 
          item.component.id === accessory.id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      );
    } else {
      setSelectedAccessories(prev => [...prev, { component: accessory, quantity: 1 }]);
    }
  };

  const removeAccessory = (accessoryId: string) => {
    setSelectedAccessories(prev => prev.filter(item => item.component.id !== accessoryId));
  };

  const updateQuantity = (accessoryId: string, quantity: number) => {
    if (quantity <= 0) {
      removeAccessory(accessoryId);
      return;
    }
    
    setSelectedAccessories(prev => 
      prev.map(item => 
        item.component.id === accessoryId 
          ? { ...item, quantity }
          : item
      )
    );
  };

  const totalPrice = selectedAccessories.reduce(
    (sum, item) => sum + (item.component.price * item.quantity), 
    0
  );

  const handleConfirm = () => {
    onConfirm(selectedAccessories);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-white rounded-2xl shadow-xl max-w-6xl w-full max-h-[90vh] overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Заголовок */}
          <div className="p-6 border-b bg-gradient-to-r from-blue-600 to-purple-600 text-white">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Выберите аксессуары</h2>
                <p className="text-blue-100 mt-1">Дополните свою конфигурацию полезными аксессуарами</p>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-white/20 rounded-lg transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          <div className="flex h-[calc(90vh-200px)]">
            {/* Левая панель - каталог аксессуаров */}
            <div className="flex-1 p-6 overflow-y-auto">
              {/* Фильтры */}
              <div className="mb-6 space-y-4">
                <input
                  type="text"
                  placeholder="Поиск аксессуаров..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="input w-full"
                />
                
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="input w-full"
                >
                  {categories.map(category => (
                    <option key={category.value} value={category.value}>
                      {category.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Список аксессуаров */}
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-2 text-gray-600">Загрузка аксессуаров...</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {filteredAccessories.map(accessory => (
                    <div key={accessory.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium text-gray-900 line-clamp-2">{accessory.name}</h4>
                        <span className="text-sm text-gray-500 ml-2">
                          {accessory.specifications?.type || 'Аксессуар'}
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-2">
                        {accessory.brand} • {accessory.model}
                      </p>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-lg font-bold text-blue-600">
                          {formatPrice(accessory.price)}
                        </span>
                        
                        <button
                          onClick={() => addAccessory(accessory)}
                          className="btn-primary flex items-center space-x-1"
                        >
                          <Plus className="w-4 h-4" />
                          <span>Добавить</span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Правая панель - выбранные аксессуары */}
            <div className="w-80 border-l bg-gray-50 p-6 overflow-y-auto">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Выбранные аксессуары ({selectedAccessories.length})
              </h3>

              {selectedAccessories.length === 0 ? (
                <div className="text-center py-8">
                  <ShoppingCart className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                  <p className="text-gray-600">Аксессуары не выбраны</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {selectedAccessories.map(item => (
                    <div key={item.component.id} className="bg-white rounded-lg p-3 border">
                      <div className="flex justify-between items-start mb-2">
                        <h5 className="font-medium text-sm line-clamp-2">{item.component.name}</h5>
                        <button
                          onClick={() => removeAccessory(item.component.id)}
                          className="text-red-500 hover:text-red-700 ml-2"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => updateQuantity(item.component.id, item.quantity - 1)}
                            className="w-6 h-6 rounded border flex items-center justify-center hover:bg-gray-100"
                          >
                            <Minus className="w-3 h-3" />
                          </button>
                          <span className="w-8 text-center">{item.quantity}</span>
                          <button
                            onClick={() => updateQuantity(item.component.id, item.quantity + 1)}
                            className="w-6 h-6 rounded border flex items-center justify-center hover:bg-gray-100"
                          >
                            <Plus className="w-3 h-3" />
                          </button>
                        </div>
                        
                        <span className="text-sm font-medium text-blue-600">
                          {formatPrice(item.component.price * item.quantity)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Итого */}
              {selectedAccessories.length > 0 && (
                <div className="mt-6 pt-4 border-t">
                  <div className="flex justify-between items-center text-lg font-bold">
                    <span>Итого:</span>
                    <span className="text-blue-600">{formatPrice(totalPrice)}</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Футер */}
          <div className="p-6 border-t bg-gray-50 flex justify-between items-center">
            <div className="text-sm text-gray-600">
              {selectedAccessories.length > 0 && (
                <span>Выбрано аксессуаров: {selectedAccessories.length}</span>
              )}
            </div>
            
            <div className="flex space-x-3">
              <button
                onClick={onClose}
                className="btn-outline"
              >
                Отмена
              </button>
              <button
                onClick={handleConfirm}
                className="btn-primary"
              >
                Продолжить с выбранными аксессуарами
              </button>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
} 