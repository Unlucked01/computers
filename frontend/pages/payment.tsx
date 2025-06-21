import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CreditCard, Shield, CheckCircle, ArrowLeft, Package, Truck } from 'lucide-react';
import Layout from '../components/Layout';
import { useRouter } from 'next/router';
import { useConfiguratorStore } from '../hooks/useConfiguratorStore';

export default function PaymentPage() {
  const [step, setStep] = useState<'form' | 'processing' | 'success'>('form');
  const [formData, setFormData] = useState({
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    cardHolder: '',
    email: '',
    phone: '',
    address: '',
  });
  const router = useRouter();
  const { selectedComponents } = useConfiguratorStore();

  // Получаем данные заказа из store
  const componentList = Object.values(selectedComponents);
  const subtotal = componentList.reduce((sum, component) => sum + component.price, 0);
  
  // Логика расчета доставки
  const FREE_DELIVERY_THRESHOLD = 150000; // 150,000 рублей
  const DELIVERY_COST = 1500;
  const deliveryCost = subtotal >= FREE_DELIVERY_THRESHOLD ? 0 : DELIVERY_COST;
  const grandTotal = subtotal + deliveryCost;

  // Если нет компонентов, перенаправляем на главную
  useEffect(() => {
    if (componentList.length === 0) {
      router.push('/');
    }
  }, [componentList.length, router]);

  const orderData = {
    items: componentList.map(component => ({
      name: `${component.brand} ${component.name}`,
      price: component.price
    })),
    total: subtotal,
    delivery: deliveryCost,
    grandTotal: grandTotal
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const formatCardNumber = (value: string) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = matches && matches[0] || '';
    const parts = [];
    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }
    if (parts.length) {
      return parts.join(' ');
    } else {
      return v;
    }
  };

  const formatExpiryDate = (value: string) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    if (v.length >= 2) {
      return v.substring(0, 2) + '/' + v.substring(2, 4);
    }
    return v;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStep('processing');
    
    // Имитация обработки платежа
    await new Promise(resolve => setTimeout(resolve, 3000));
    setStep('success');
  };

  const isFormValid = formData.cardNumber.length >= 19 && 
                     formData.expiryDate.length >= 5 && 
                     formData.cvv.length >= 3 && 
                     formData.cardHolder.length >= 2 &&
                     formData.email.length >= 5 &&
                     formData.phone.length >= 10;

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-4xl mx-auto"
          >
            {step === 'form' && (
              <>
                {/* Заголовок */}
                <div className="text-center mb-8">
                  <h1 className="text-3xl font-bold text-gray-900 mb-4">
                    Оформление заказа
                  </h1>
                  <p className="text-gray-600">
                    Завершите покупку вашей конфигурации ПК
                  </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Форма оплаты */}
                  <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="bg-white rounded-2xl shadow-xl p-8"
                  >
                    <div className="flex items-center space-x-3 mb-6">
                      <CreditCard className="w-6 h-6 text-blue-600" />
                      <h2 className="text-xl font-semibold text-gray-900">
                        Данные для оплаты
                      </h2>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                      {/* Номер карты */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Номер карты
                        </label>
                        <input
                          type="text"
                          value={formData.cardNumber}
                          onChange={(e) => handleInputChange('cardNumber', formatCardNumber(e.target.value))}
                          placeholder="1234 5678 9012 3456"
                          maxLength={19}
                          className="input w-full"
                          required
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        {/* Срок действия */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Срок действия
                          </label>
                          <input
                            type="text"
                            value={formData.expiryDate}
                            onChange={(e) => handleInputChange('expiryDate', formatExpiryDate(e.target.value))}
                            placeholder="MM/YY"
                            maxLength={5}
                            className="input w-full"
                            required
                          />
                        </div>

                        {/* CVV */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            CVV
                          </label>
                          <input
                            type="text"
                            value={formData.cvv}
                            onChange={(e) => handleInputChange('cvv', e.target.value.replace(/\D/g, ''))}
                            placeholder="123"
                            maxLength={3}
                            className="input w-full"
                            required
                          />
                        </div>
                      </div>

                      {/* Имя держателя карты */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Имя держателя карты
                        </label>
                        <input
                          type="text"
                          value={formData.cardHolder}
                          onChange={(e) => handleInputChange('cardHolder', e.target.value)}
                          placeholder="IVAN PETROV"
                          className="input w-full"
                          required
                        />
                      </div>

                      {/* Email */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Email для чека
                        </label>
                        <input
                          type="email"
                          value={formData.email}
                          onChange={(e) => handleInputChange('email', e.target.value)}
                          placeholder="ivan@example.com"
                          className="input w-full"
                          required
                        />
                      </div>

                      {/* Телефон */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Телефон
                        </label>
                        <input
                          type="tel"
                          value={formData.phone}
                          onChange={(e) => handleInputChange('phone', e.target.value)}
                          placeholder="+7 (999) 123-45-67"
                          className="input w-full"
                          required
                        />
                      </div>

                      {/* Адрес доставки */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Адрес доставки
                        </label>
                        <textarea
                          value={formData.address}
                          onChange={(e) => handleInputChange('address', e.target.value)}
                          placeholder="Москва, ул. Примерная, д. 123, кв. 45"
                          className="input w-full h-20 resize-none"
                          required
                        />
                      </div>

                      {/* Безопасность */}
                      <div className="flex items-center space-x-2 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                        <Shield className="w-4 h-4 text-green-600" />
                        <span>Ваши данные защищены SSL-шифрованием</span>
                      </div>

                      {/* Кнопка оплаты */}
                      <button
                        type="submit"
                        disabled={!isFormValid}
                        className="btn-primary w-full py-4 text-lg"
                      >
                        Оплатить {orderData.grandTotal.toLocaleString()} ₽
                      </button>
                    </form>
                  </motion.div>

                  {/* Сводка заказа */}
                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="bg-white rounded-2xl shadow-xl p-8"
                  >
                    <h2 className="text-xl font-semibold text-gray-900 mb-6">
                      Ваш заказ
                    </h2>

                    <div className="space-y-4">
                      {orderData.items.map((item, index) => (
                        <div key={index} className="flex justify-between items-center py-2 border-b">
                          <span className="text-gray-700">{item.name}</span>
                          <span className="font-medium">{item.price.toLocaleString()} ₽</span>
                        </div>
                      ))}
                      
                      <div className="flex justify-between items-center py-2">
                        <span className="text-gray-700">Доставка</span>
                        <span className="font-medium">
                          {orderData.delivery === 0 ? 'Бесплатно' : `${orderData.delivery.toLocaleString()} ₽`}
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center py-3 border-t-2 text-lg font-bold">
                        <span>Итого</span>
                        <span className="text-green-600">{orderData.grandTotal.toLocaleString()} ₽</span>
                      </div>
                    </div>

                    {/* Информация о доставке */}
                    <div className={`mt-6 p-4 rounded-lg ${
                      orderData.delivery === 0 ? 'bg-green-50' : 'bg-blue-50'
                    }`}>
                      <div className="flex items-center space-x-2 mb-2">
                        <Truck className={`w-5 h-5 ${
                          orderData.delivery === 0 ? 'text-green-600' : 'text-blue-600'
                        }`} />
                        <span className={`font-medium ${
                          orderData.delivery === 0 ? 'text-green-900' : 'text-blue-900'
                        }`}>
                          {orderData.delivery === 0 ? 'Бесплатная доставка!' : 'Доставка'}
                        </span>
                      </div>
                      {orderData.delivery === 0 ? (
                        <p className="text-sm text-green-700">
                          🎉 Поздравляем! Ваш заказ превышает 150 000 ₽ - доставка бесплатно!
                        </p>
                      ) : (
                        <p className="text-sm text-blue-700">
                          Бесплатная доставка при заказе от 150 000 ₽ 
                          (до бесплатной доставки осталось: {(FREE_DELIVERY_THRESHOLD - subtotal).toLocaleString()} ₽)
                        </p>
                      )}
                      <p className={`text-sm ${
                        orderData.delivery === 0 ? 'text-green-700' : 'text-blue-700'
                      }`}>
                        Срок доставки: 2-3 рабочих дня
                      </p>
                    </div>
                  </motion.div>
                </div>
              </>
            )}

            {step === 'processing' && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center py-16"
              >
                <div className="bg-white rounded-2xl shadow-xl p-12 max-w-md mx-auto">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-6"></div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Обработка платежа
                  </h2>
                  <p className="text-gray-600">
                    Пожалуйста, подождите. Не закрывайте страницу.
                  </p>
                </div>
              </motion.div>
            )}

            {step === 'success' && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center py-16"
              >
                <div className="bg-white rounded-2xl shadow-xl p-12 max-w-2xl mx-auto">
                  <CheckCircle className="w-20 h-20 text-green-500 mx-auto mb-6" />
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">
                    Заказ успешно оформлен!
                  </h2>
                  <p className="text-gray-600 mb-8">
                    Номер заказа: <span className="font-mono font-bold">#PC-2024-001</span>
                  </p>
                  
                  <div className="bg-gray-50 rounded-lg p-6 mb-8 text-left">
                    <h3 className="font-semibold text-gray-900 mb-4">Что дальше?</h3>
                    <div className="space-y-3">
                      <div className="flex items-center space-x-3">
                        <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                          <span className="text-white text-sm font-bold">1</span>
                        </div>
                        <span className="text-gray-700">Мы отправили подтверждение на ваш email</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                          <span className="text-white text-sm font-bold">2</span>
                        </div>
                        <span className="text-gray-700">Сборка и тестирование займет 1-2 дня</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                          <span className="text-white text-sm font-bold">3</span>
                        </div>
                        <span className="text-gray-700">Доставка курьером в течение 2-3 дней</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex space-x-4">
                    <button
                      onClick={() => router.push('/')}
                      className="btn-outline flex-1 flex items-center justify-center space-x-2"
                    >
                      <ArrowLeft className="w-4 h-4" />
                      <span>На главную</span>
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>
    </Layout>
  );
} 