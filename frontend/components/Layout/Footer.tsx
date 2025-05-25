import React from 'react';
import { Monitor } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="container py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Логотип и описание */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Monitor className="h-8 w-8 text-blue-400" />
              <span className="text-xl font-bold">PC Builder</span>
            </div>
            <p className="text-gray-400 max-w-md">
              Современный конфигуратор персональных компьютеров с проверкой 
              совместимости компонентов и отслеживанием наличия.
            </p>
          </div>

          {/* Быстрые ссылки */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Навигация</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-gray-400 hover:text-white transition-colors">
                  Конфигуратор
                </a>
              </li>
              <li>
                <a href="/about" className="text-gray-400 hover:text-white transition-colors">
                  О проекте
                </a>
              </li>
              <li>
                <a href="/accessories" className="text-gray-400 hover:text-white transition-colors">
                  Аксессуары
                </a>
              </li>
              <li>
                <a href="/software" className="text-gray-400 hover:text-white transition-colors">
                  Программы
                </a>
              </li>
            </ul>
          </div>

          {/* Информация */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Проект</h3>
            <ul className="space-y-2">
              <li>
                <span className="text-gray-400">Дипломная работа</span>
              </li>
              <li>
                <span className="text-gray-400">Бакалавриат</span>
              </li>
              <li>
                <span className="text-gray-400">2024 год</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Нижняя часть */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © 2024 PC Builder. Дипломный проект.
            </p>
            <p className="text-gray-400 text-sm mt-2 md:mt-0">
              Создано с использованием Next.js и FastAPI
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
} 