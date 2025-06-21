import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Layout from '../components/Layout';
import { 
  Mouse, 
  Keyboard, 
  Monitor, 
  Headphones, 
  Camera, 
  Gamepad2,
  Filter,
  Search,
  ShoppingCart,
  Check,
  Clock,
  AlertTriangle
} from 'lucide-react';

interface Accessory {
  id: string;
  name: string;
  brand: string;
  model: string;
  description: string;
  price: number;
  specifications: {
    type: string;
    connection?: string;
    [key: string]: any;
  };
  stock?: {
    status: 'in_stock' | 'expected' | 'out_of_stock';
    quantity: number;
    expected_date?: string;
  };
}

interface AccessoryCategory {
  slug: string;
  name: string;
  count: number;
}

interface FilterOptions {
  brands: string[];
  types: string[];
  connections: string[];
  price_range: {
    min: number;
    max: number;
  };
}

export default function Accessories() {
  const [accessories, setAccessories] = useState<Accessory[]>([]);
  const [categories, setCategories] = useState<AccessoryCategory[]>([]);
  const [filterOptions, setFilterOptions] = useState<FilterOptions | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Фильтры
  const [selectedType, setSelectedType] = useState<string>('');
  const [selectedBrand, setSelectedBrand] = useState<string>('');
  const [selectedConnection, setSelectedConnection] = useState<string>('');
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 100000]);
  const [onlyInStock, setOnlyInStock] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Загрузка данных
  useEffect(() => {
    loadAccessories();
    loadCategories();
    loadFilterOptions();
  }, []);

  // Применение фильтров
  useEffect(() => {
    loadAccessories();
  }, [selectedType, selectedBrand, selectedConnection, priceRange, onlyInStock, searchQuery]);

  const loadAccessories = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      if (selectedType) params.append('type_filter', selectedType);
      if (selectedBrand) params.append('brand', selectedBrand);
      if (selectedConnection) params.append('connection', selectedConnection);
      if (priceRange[0] > 0) params.append('price_min', priceRange[0].toString());
      if (priceRange[1] < 100000) params.append('price_max', priceRange[1].toString());
      if (onlyInStock) params.append('only_in_stock', 'true');
      if (searchQuery) params.append('search', searchQuery);
      params.append('limit', '50');

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/accessories?${params}`);
      if (!response.ok) throw new Error('Ошибка загрузки аксессуаров');
      
      const data = await response.json();
      setAccessories(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Неизвестная ошибка');
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/accessories/categories`);
      if (!response.ok) throw new Error('Ошибка загрузки категорий');
      
      const data = await response.json();
      setCategories(data);
    } catch (err) {
      console.error('Ошибка загрузки категорий:', err);
    }
  };

  const loadFilterOptions = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/accessories/filters/options`);
      if (!response.ok) throw new Error('Ошибка загрузки опций фильтров');
      
      const data = await response.json();
      setFilterOptions(data);
      setPriceRange([data.price_range.min, data.price_range.max]);
    } catch (err) {
      console.error('Ошибка загрузки опций фильтров:', err);
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'mouse': return <Mouse className="w-5 h-5" />;
      case 'keyboard': return <Keyboard className="w-5 h-5" />;
      case 'monitor': return <Monitor className="w-5 h-5" />;
      case 'headset':
      case 'headphones': return <Headphones className="w-5 h-5" />;
      case 'webcam': return <Camera className="w-5 h-5" />;
      case 'mousepad': return <Gamepad2 className="w-5 h-5" />;
      default: return <Gamepad2 className="w-5 h-5" />;
    }
  };

  const getStockStatus = (stock: Accessory['stock']) => {
    if (!stock) return { icon: <AlertTriangle className="w-4 h-4 text-gray-400" />, text: 'Нет данных', color: 'text-gray-400' };
    
    switch (stock.status) {
      case 'in_stock':
        return { icon: <Check className="w-4 h-4 text-green-500" />, text: 'В наличии', color: 'text-green-500' };
      case 'expected':
        return { icon: <Clock className="w-4 h-4 text-yellow-500" />, text: 'Ожидается', color: 'text-yellow-500' };
      case 'out_of_stock':
        return { icon: <AlertTriangle className="w-4 h-4 text-red-500" />, text: 'Нет в наличии', color: 'text-red-500' };
      default:
        return { icon: <AlertTriangle className="w-4 h-4 text-gray-400" />, text: 'Неизвестно', color: 'text-gray-400' };
    }
  };

  const clearFilters = () => {
    setSelectedType('');
    setSelectedBrand('');
    setSelectedConnection('');
    setPriceRange(filterOptions ? [filterOptions.price_range.min, filterOptions.price_range.max] : [0, 100000]);
    setOnlyInStock(false);
    setSearchQuery('');
  };

  return (
    <>
      <Head>
        <title>Аксессуары - PC Configurator</title>
        <meta name="description" content="Каталог аксессуаров для ПК: мыши, клавиатуры, мониторы, наушники и другие периферийные устройства" />
      </Head>

      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
          {/* Hero секция */}
          <section className="pt-20 pb-16">
            <div className="container">
              <div className="text-center mb-16">
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                  Аксессуары
                  <span className="text-gradient"> для ПК</span>
                </h1>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  Широкий выбор периферийных устройств: мыши, клавиатуры, мониторы, 
                  наушники и другие аксессуары для комфортной работы и игр
                </p>
              </div>
            </div>
          </section>

          {/* Категории */}
          <section className="py-8 bg-white">
            <div className="container">
              <div className="flex flex-wrap gap-4 justify-center">
                <button
                  onClick={() => setSelectedType('')}
                  className={`px-6 py-3 rounded-full transition-all duration-200 ${
                    selectedType === '' 
                      ? 'bg-blue-600 text-white shadow-lg' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Все категории
                </button>
                {categories.map((category) => (
                  <button
                    key={category.slug}
                    onClick={() => setSelectedType(category.slug)}
                    className={`px-6 py-3 rounded-full transition-all duration-200 flex items-center space-x-2 ${
                      selectedType === category.slug 
                        ? 'bg-blue-600 text-white shadow-lg' 
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {getTypeIcon(category.slug)}
                    <span>{category.name}</span>
                    <span className="text-xs opacity-75">({category.count})</span>
                  </button>
                ))}
              </div>
            </div>
          </section>

          {/* Фильтры и поиск */}
          <section className="py-8">
            <div className="container">
              <div className="bg-white rounded-2xl p-6 shadow-lg mb-8">
                <div className="flex flex-wrap gap-4 items-center">
                  {/* Поиск */}
                  <div className="flex-1 min-w-64">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                      <input
                        type="text"
                        placeholder="Поиск аксессуаров..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  {/* Фильтр по бренду */}
                  {filterOptions && (
                    <select
                      value={selectedBrand}
                      onChange={(e) => setSelectedBrand(e.target.value)}
                      className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Все бренды</option>
                      {filterOptions.brands.map((brand) => (
                        <option key={brand} value={brand}>{brand}</option>
                      ))}
                    </select>
                  )}

                  {/* Фильтр по подключению */}
                  {filterOptions && (
                    <select
                      value={selectedConnection}
                      onChange={(e) => setSelectedConnection(e.target.value)}
                      className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Все типы подключения</option>
                      {filterOptions.connections.map((connection) => (
                        <option key={connection} value={connection}>
                          {connection === 'wired' ? 'Проводное' : connection === 'wireless' ? 'Беспроводное' : connection}
                        </option>
                      ))}
                    </select>
                  )}

                  {/* Только в наличии */}
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={onlyInStock}
                      onChange={(e) => setOnlyInStock(e.target.checked)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">Только в наличии</span>
                  </label>

                  {/* Очистить фильтры */}
                  <button
                    onClick={clearFilters}
                    className="px-4 py-2 text-gray-600 hover:text-blue-600 transition-colors duration-200"
                  >
                    Очистить
                  </button>
                </div>
              </div>
            </div>
          </section>

          {/* Список аксессуаров */}
          <section className="pb-20">
            <div className="container">
              {loading ? (
                <div className="text-center py-12">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-4 text-gray-600">Загрузка аксессуаров...</p>
                </div>
              ) : error ? (
                <div className="text-center py-12">
                  <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
                  <p className="text-red-600">{error}</p>
                </div>
              ) : accessories.length === 0 ? (
                <div className="text-center py-12">
                  <Filter className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">Аксессуары не найдены</p>
                  <p className="text-sm text-gray-500 mt-2">Попробуйте изменить фильтры поиска</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {accessories.map((accessory) => {
                    const stockStatus = getStockStatus(accessory.stock);
                    return (
                      <div key={accessory.id} className="card p-6 hover:shadow-lg transition-shadow duration-300">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center space-x-2">
                            {getTypeIcon(accessory.specifications.type)}
                            <span className="text-sm text-gray-500 capitalize">
                              {accessory.specifications.type}
                            </span>
                          </div>
                          <div className={`flex items-center space-x-1 ${stockStatus.color}`}>
                            {stockStatus.icon}
                            <span className="text-xs">{stockStatus.text}</span>
                          </div>
                        </div>

                        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                          {accessory.name}
                        </h3>

                        <p className="text-sm text-gray-600 mb-2">
                          {accessory.brand} • {accessory.model}
                        </p>

                        <p className="text-sm text-gray-500 mb-4 line-clamp-2">
                          {accessory.description}
                        </p>

                        {/* Характеристики */}
                        <div className="space-y-1 mb-4 text-xs text-gray-600">
                          {accessory.specifications.connection && (
                            <div>Подключение: {accessory.specifications.connection === 'wired' ? 'Проводное' : 'Беспроводное'}</div>
                          )}
                          {accessory.specifications.dpi && (
                            <div>DPI: {accessory.specifications.dpi.toLocaleString()}</div>
                          )}
                          {accessory.specifications.size_inch && (
                            <div>Размер: {accessory.specifications.size_inch}"</div>
                          )}
                          {accessory.specifications.resolution && (
                            <div>Разрешение: {accessory.specifications.resolution}</div>
                          )}
                        </div>

                        <div className="flex items-center justify-between">
                          <div className="text-xl font-bold text-blue-600">
                            {accessory.price.toLocaleString()} ₽
                          </div>

                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </section>
        </div>
      </Layout>
    </>
  );
} 