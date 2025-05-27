import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Layout from '../components/Layout';
import { 
  Cpu, 
  HardDrive, 
  Monitor, 
  Zap,
  Box,
  Fan,
  MemoryStick,
  Gamepad2,
  ChevronDown,
  ChevronUp,
  Package
} from 'lucide-react';

interface Component {
  id: string;
  name: string;
  brand: string;
  model: string;
  description: string;
  price: number;
  category: {
    name: string;
    slug: string;
  };
  specifications: any;
  stock?: {
    status: 'in_stock' | 'expected' | 'out_of_stock';
    quantity: number;
  };
}

interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  icon: string;
}

export default function Components() {
  const [components, setComponents] = useState<Component[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Загружаем категории
      const categoriesResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/categories`);
      const categoriesData = await categoriesResponse.json();
      setCategories(categoriesData);

      // Загружаем все компоненты
      const componentsResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/components?limit=100`);
      const componentsData = await componentsResponse.json();
      setComponents(componentsData);
      
    } catch (err) {
      console.error('Ошибка загрузки данных:', err);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (iconName: string) => {
    switch (iconName) {
      case 'cpu': return <Cpu className="w-6 h-6" />;
      case 'motherboard': return <Package className="w-6 h-6" />;
      case 'memory': return <MemoryStick className="w-6 h-6" />;
      case 'gpu': return <Monitor className="w-6 h-6" />;
      case 'storage': return <HardDrive className="w-6 h-6" />;
      case 'power': return <Zap className="w-6 h-6" />;
      case 'case': return <Box className="w-6 h-6" />;
      case 'fan': return <Fan className="w-6 h-6" />;
      case 'accessories': return <Gamepad2 className="w-6 h-6" />;
      default: return <Package className="w-6 h-6" />;
    }
  };

  const getComponentsByCategory = (categorySlug: string) => {
    return components.filter(component => component.category.slug === categorySlug);
  };

  const toggleCategory = (categorySlug: string) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(categorySlug)) {
      newExpanded.delete(categorySlug);
    } else {
      newExpanded.add(categorySlug);
    }
    setExpandedCategories(newExpanded);
  };

  const getStockBadge = (stock: Component['stock']) => {
    if (!stock) return <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">Нет данных</span>;
    
    switch (stock.status) {
      case 'in_stock':
        return <span className="px-2 py-1 text-xs bg-green-100 text-green-700 rounded">В наличии ({stock.quantity})</span>;
      case 'expected':
        return <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-700 rounded">Ожидается</span>;
      case 'out_of_stock':
        return <span className="px-2 py-1 text-xs bg-red-100 text-red-700 rounded">Нет в наличии</span>;
      default:
        return <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">Неизвестно</span>;
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Загрузка компонентов...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <>
      <Head>
        <title>Все компоненты - PC Configurator</title>
        <meta name="description" content="Полный каталог компонентов для сборки ПК" />
      </Head>

      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
          {/* Hero секция */}
          <section className="pt-20 pb-16">
            <div className="container">
              <div className="text-center mb-16">
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                  Каталог
                  <span className="text-gradient"> компонентов</span>
                </h1>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  Полный список всех доступных компонентов для сборки персональных компьютеров
                </p>
              </div>
            </div>
          </section>

          {/* Статистика */}
          <section className="py-8 bg-white">
            <div className="container">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{categories.length}</div>
                  <div className="text-sm text-gray-600">Категорий</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">{components.length}</div>
                  <div className="text-sm text-gray-600">Компонентов</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600">
                    {components.filter(c => c.stock?.status === 'in_stock').length}
                  </div>
                  <div className="text-sm text-gray-600">В наличии</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600">
                    {new Set(components.map(c => c.brand)).size}
                  </div>
                  <div className="text-sm text-gray-600">Брендов</div>
                </div>
              </div>
            </div>
          </section>

          {/* Список категорий и компонентов */}
          <section className="py-16">
            <div className="container">
              <div className="space-y-6">
                {categories.map((category) => {
                  const categoryComponents = getComponentsByCategory(category.slug);
                  const isExpanded = expandedCategories.has(category.slug);
                  
                  return (
                    <div key={category.id} className="bg-white rounded-2xl shadow-lg overflow-hidden">
                      <button
                        onClick={() => toggleCategory(category.slug)}
                        className="w-full p-6 flex items-center justify-between hover:bg-gray-50 transition-colors duration-200"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="p-3 bg-blue-100 rounded-lg text-blue-600">
                            {getCategoryIcon(category.icon)}
                          </div>
                          <div className="text-left">
                            <h3 className="text-xl font-semibold text-gray-900">{category.name}</h3>
                            <p className="text-gray-600">{category.description}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-4">
                          <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                            {categoryComponents.length} компонентов
                          </span>
                          {isExpanded ? (
                            <ChevronUp className="w-5 h-5 text-gray-400" />
                          ) : (
                            <ChevronDown className="w-5 h-5 text-gray-400" />
                          )}
                        </div>
                      </button>

                      {isExpanded && (
                        <div className="border-t border-gray-200">
                          <div className="p-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                              {categoryComponents.map((component) => (
                                <div key={component.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
                                  <div className="flex justify-between items-start mb-2">
                                    <h4 className="font-semibold text-gray-900 text-sm line-clamp-2">
                                      {component.name}
                                    </h4>
                                    {getStockBadge(component.stock)}
                                  </div>
                                  
                                  <p className="text-xs text-gray-600 mb-2">
                                    {component.brand} • {component.model}
                                  </p>
                                  
                                  <p className="text-xs text-gray-500 mb-3 line-clamp-2">
                                    {component.description}
                                  </p>
                                  
                                  <div className="flex justify-between items-center">
                                    <span className="text-lg font-bold text-blue-600">
                                      {component.price.toLocaleString()} ₽
                                    </span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </section>
        </div>
      </Layout>
    </>
  );
} 