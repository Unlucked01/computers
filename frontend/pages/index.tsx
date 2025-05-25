import React from 'react';
import Head from 'next/head';
import Layout from '../components/Layout';
import Configurator from '../components/Configurator';

export default function Home() {
  return (
    <>
      <Head>
        <title>PC Configurator - Создайте свой идеальный компьютер</title>
        <meta name="description" content="Конфигуратор персональных компьютеров с проверкой совместимости компонентов" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
          {/* Hero секция */}
          <section className="pt-20 pb-16">
            <div className="container">
              <div className="text-center mb-12">
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                  Создайте свой
                  <span className="text-gradient"> идеальный </span>
                  компьютер
                </h1>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  Профессиональный конфигуратор ПК с проверкой совместимости компонентов, 
                  отслеживанием наличия и современным интерфейсом
                </p>
              </div>
            </div>
          </section>

          {/* Основной конфигуратор */}
          <section className="pb-20">
            <div className="container">
              <Configurator />
            </div>
          </section>
        </div>
      </Layout>
    </>
  );
} 