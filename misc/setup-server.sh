#!/bin/bash

# Главный скрипт для настройки сервера с системными сервисами

echo "🚀 Настройка сервера для PC Configurator и Events..."
echo "Этот скрипт установит и настроит:"
echo "  - PostgreSQL как системный сервис"
echo "  - Nginx как системный сервис"
echo "  - SSL сертификаты"
echo ""

read -p "Продолжить? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Отменено"
    exit 1
fi

# Проверяем права sudo
if ! sudo -n true 2>/dev/null; then
    echo "❌ Требуются права sudo"
    exit 1
fi

echo ""
echo "📋 Шаг 1: Установка и настройка PostgreSQL..."
chmod +x setup-postgres.sh
./setup-postgres.sh

if [ $? -ne 0 ]; then
    echo "❌ Ошибка настройки PostgreSQL"
    exit 1
fi

echo ""
echo "📋 Шаг 2: Установка и настройка Nginx..."
chmod +x setup-nginx.sh
./setup-nginx.sh

if [ $? -ne 0 ]; then
    echo "❌ Ошибка настройки Nginx"
    exit 1
fi

echo ""
echo "📋 Шаг 3: Запуск PC Configurator..."
docker-compose down 2>/dev/null || true
docker-compose up -d --build

echo ""
echo "⏳ Ожидание запуска сервисов (30 секунд)..."
sleep 30

echo ""
echo "📋 Шаг 4: Проверка статуса..."

# Проверяем PostgreSQL
echo "PostgreSQL статус:"
sudo systemctl status postgresql --no-pager -l

echo ""
echo "Nginx статус:"
sudo systemctl status nginx --no-pager -l

echo ""
echo "Docker контейнеры:"
docker-compose ps

echo ""
echo "📋 Шаг 5: Тестирование подключений..."

# Тест PostgreSQL
echo "Тест PostgreSQL:"
if psql -h localhost -U postgres -d pc_configurator -c "SELECT 1;" >/dev/null 2>&1; then
    echo "✅ PostgreSQL доступен"
else
    echo "❌ PostgreSQL недоступен"
fi

# Тест backend API
echo "Тест Backend API:"
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Backend API доступен"
else
    echo "❌ Backend API недоступен"
fi

# Тест frontend
echo "Тест Frontend:"
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    echo "✅ Frontend доступен"
else
    echo "❌ Frontend недоступен"
fi

echo ""
echo "🎉 Базовая настройка завершена!"
echo ""
echo "📝 Следующие шаги:"
echo "1. Получите SSL сертификаты: chmod +x setup-ssl.sh && ./setup-ssl.sh"
echo "2. Проверьте доступность сайтов:"
echo "   - http://unl-computers.duckdns.org"
echo "   - http://unl-events.duckdns.org (если events запущен)"
echo ""
echo "📊 Полезные команды:"
echo "  - Статус PostgreSQL: sudo systemctl status postgresql"
echo "  - Статус Nginx: sudo systemctl status nginx"
echo "  - Логи Nginx: sudo tail -f /var/log/nginx/error.log"
echo "  - Перезапуск Nginx: sudo systemctl reload nginx"
echo "  - Статус контейнеров: docker-compose ps" 