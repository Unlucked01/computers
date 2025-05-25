#!/bin/bash

# Простой скрипт деплоя PC Configurator

set -e

echo "🚀 Деплой PC Configurator..."

# Проверяем что сеть app_network существует
if ! docker network ls | grep -q "app_network"; then
    echo "❌ Сеть app_network не найдена!"
    echo "📝 Убедитесь что проект events запущен"
    exit 1
fi

# Проверяем что PostgreSQL контейнер запущен
if ! docker ps | grep -q "events-db"; then
    echo "❌ PostgreSQL контейнер events-db не найден!"
    echo "📝 Убедитесь что проект events запущен"
    exit 1
fi

echo "🔨 Собираем образы..."
docker-compose build --no-cache

echo "🚀 Запускаем сервисы..."
docker-compose up -d

echo "⏳ Ждем запуска сервисов..."
sleep 15

echo "📊 Статус сервисов:"
docker-compose ps

echo ""
echo "✅ Деплой завершен!"
echo "🌐 После настройки Nginx приложение будет доступно:"
echo "    https://unl-computers.duckdns.org"
echo ""
echo "📋 Следующие шаги:"
echo "1. Создайте базу данных pc_configurator в PostgreSQL"
echo "2. Обновите nginx.conf в проекте events"
echo "3. Получите SSL сертификат для unl-computers.duckdns.org"
echo "4. Перезапустите Nginx"
echo ""
echo "📖 Подробные инструкции в файле: nginx-update-instructions.md" 