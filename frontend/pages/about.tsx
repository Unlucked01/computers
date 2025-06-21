import React from 'react';
import Head from 'next/head';
import Layout from '../components/Layout';
import { 
  Monitor, 
  Code, 
  Database, 
  Palette, 
  CheckCircle, 
  Users, 
  Zap,
  Shield,
  Globe,
  Settings
} from 'lucide-react';

export default function About() {
  const technologies = [
    {
      name: 'Frontend',
      items: [
        { name: 'Next.js 14', description: 'React фреймворк с SSR' },
        { name: 'TypeScript', description: 'Статическая типизация' },
        { name: 'Tailwind CSS', description: 'Utility-first CSS фреймворк' },
        { name: 'Framer Motion', description: 'Анимации и интерактивность' },
        { name: 'React Query', description: 'Управление состоянием данных' },
        { name: 'Zustand', description: 'Глобальное состояние приложения' },
      ],
      icon: <Monitor className="w-6 h-6" />,
      color: 'from-blue-500 to-cyan-500',
    },
    {
      name: 'Backend',
      items: [
        { name: 'Python 3.11+', description: 'Основной язык разработки' },
        { name: 'FastAPI', description: 'Современный веб-фреймворк' },
        { name: 'PostgreSQL', description: 'Реляционная база данных' },
        { name: 'SQLAlchemy', description: 'ORM для работы с БД' },
        { name: 'Pydantic', description: 'Валидация данных' },
        { name: 'Alembic', description: 'Миграции базы данных' },
      ],
      icon: <Database className="w-6 h-6" />,
      color: 'from-green-500 to-emerald-500',
    },
    {
      name: 'DevOps & Tools',
      items: [
        { name: 'Docker', description: 'Контейнеризация приложения' },
        { name: 'Git', description: 'Система контроля версий' },
        { name: 'ESLint', description: 'Статический анализ кода' },
        { name: 'Prettier', description: 'Форматирование кода' },
        { name: 'Swagger/OpenAPI', description: 'Документация API' },
      ],
      icon: <Settings className="w-6 h-6" />,
      color: 'from-purple-500 to-pink-500',
    },
  ];

  const features = [
    {
      icon: <Zap className="w-8 h-8 text-yellow-500" />,
      title: 'Проверка совместимости',
      description: 'Автоматическая проверка совместимости выбранных компонентов с учетом характеристик',
    },
    {
      icon: <Shield className="w-8 h-8 text-green-500" />,
      title: 'Отслеживание наличия',
      description: 'Мониторинг наличия компонентов в режиме реального времени',
    },
    {
      icon: <Globe className="w-8 h-8 text-blue-500" />,
      title: 'Современный интерфейс',
      description: 'Адаптивный дизайн с поддержкой мобильных устройств',
    },
    {
      icon: <Code className="w-8 h-8 text-purple-500" />,
      title: 'Экспорт конфигураций',
      description: 'Сохранение и экспорт конфигураций в различных форматах',
    },
  ];

  return (
    <>
      <Head>
        <title>О проекте - PC Configurator</title>
        <meta name="description" content="Информация о дипломном проекте веб-конфигуратора персональных компьютеров" />
      </Head>

      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
          {/* Hero секция */}
          <section className="pt-20 pb-16">
            <div className="container">
              <div className="text-center mb-16">
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                  О проекте
                  <span className="text-gradient"> PC Builder</span>
                </h1>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  Дипломный проект бакалавра по созданию современного веб-конфигуратора 
                  персональных компьютеров с проверкой совместимости компонентов
                </p>
              </div>
            </div>
          </section>

          {/* Описание проекта */}
          <section className="py-16">
            <div className="container">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-6">
                    Цель проекта
                  </h2>
                  <div className="space-y-4 text-gray-600">
                    <p>
                      Создание современного веб-приложения для конфигурирования персональных 
                      компьютеров, которое поможет пользователям подобрать совместимые 
                      компоненты и собрать оптимальную конфигурацию ПК.
                    </p>
                    <p>
                      Проект решает проблему сложности выбора совместимых компонентов при 
                      самостоятельной сборке компьютера, предоставляя интуитивный интерфейс 
                      и автоматическую проверку совместимости.
                    </p>
                    <p>
                      Дипломная работа демонстрирует применение современных технологий 
                      веб-разработки для создания практически значимого продукта.
                    </p>
                  </div>
                </div>
                <div className="bg-white p-8 rounded-2xl shadow-xl">
                  <div className="grid grid-cols-2 gap-6">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-600">2025</div>
                      <div className="text-sm text-gray-600">Год разработки</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-600">8+</div>
                      <div className="text-sm text-gray-600">Категорий компонентов</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-purple-600">100%</div>
                      <div className="text-sm text-gray-600">Проверка совместимости</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-red-600">∞</div>
                      <div className="text-sm text-gray-600">Конфигураций</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Функциональность */}
          <section className="py-16 bg-white">
            <div className="container">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Ключевые возможности
                </h2>
                <p className="text-xl text-gray-600">
                  Функции, которые делают конфигуратор удобным и надежным
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                {features.map((feature, index) => (
                  <div 
                    key={index}
                    className="card p-6 text-center hover:shadow-lg transition-shadow duration-300"
                  >
                    <div className="flex justify-center mb-4">
                      {feature.icon}
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 text-sm">
                      {feature.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Технологии */}
          <section className="py-16">
            <div className="container">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Технологический стек
                </h2>
                <p className="text-xl text-gray-600">
                  Современные технологии для создания качественного продукта
                </p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {technologies.map((tech, index) => (
                  <div key={index} className="card p-6">
                    <div className="flex items-center mb-6">
                      <div className={`p-3 rounded-lg bg-gradient-to-r ${tech.color} text-white mr-4`}>
                        {tech.icon}
                      </div>
                      <h3 className="text-xl font-bold text-gray-900">
                        {tech.name}
                      </h3>
                    </div>
                    
                    <div className="space-y-3">
                      {tech.items.map((item, itemIndex) => (
                        <div key={itemIndex} className="flex items-start space-x-3">
                          <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                          <div>
                            <div className="font-medium text-gray-900">
                              {item.name}
                            </div>
                            <div className="text-sm text-gray-600">
                              {item.description}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Архитектура */}
          <section className="py-16 bg-gray-50">
            <div className="container">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Архитектура приложения
                </h2>
                <p className="text-xl text-gray-600">
                  Современная клиент-серверная архитектура с разделением frontend и backend
                </p>
              </div>

              <div className="bg-white rounded-2xl p-8 shadow-lg">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  <div className="text-center">
                    <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Monitor className="w-10 h-10 text-blue-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      Frontend (Next.js)
                    </h3>
                    <p className="text-gray-600 text-sm">
                      Пользовательский интерфейс с серверным рендерингом, 
                      современными компонентами и адаптивным дизайном
                    </p>
                  </div>

                  <div className="text-center">
                    <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Database className="w-10 h-10 text-green-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      Backend (FastAPI)
                    </h3>
                    <p className="text-gray-600 text-sm">
                      REST API с автоматической документацией, валидацией данных 
                      и логикой проверки совместимости
                    </p>
                  </div>

                  <div className="text-center">
                    <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Settings className="w-10 h-10 text-purple-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      Database (PostgreSQL)
                    </h3>
                    <p className="text-gray-600 text-sm">
                      Реляционная база данных для хранения информации о компонентах, 
                      совместимости и конфигурациях
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* О разработчике */}
          <section className="py-16">
            <div className="container">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  О разработчике
                </h2>
              </div>

              <div className="max-w-4xl mx-auto">
                <div className="card p-8 text-center">
                  <div className="w-32 h-32 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6">
                    <Users className="w-16 h-16 text-white" />
                  </div>
                  
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">
                    Дипломный проект Анохина М.А.
                  </h3>
                  
                  <div className="text-gray-600 space-y-2 mb-6">
                    <p>Специальность: Программная инженерия</p>
                    <p>Год защиты: 2025</p>
                  </div>

                  <div className="flex justify-center space-x-4">
                    <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm">
                      Frontend Development
                    </span>
                    <span className="px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm">
                      Backend Development
                    </span>
                    <span className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm">
                      System Design
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </Layout>
    </>
  );
} 