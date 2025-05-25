#!/bin/bash

# Скрипт для исправления проблем с развертыванием PC Configurator

echo "🔧 Исправление проблем с развертыванием PC Configurator..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Убедитесь, что вы в корне проекта PC Configurator."
    exit 1
fi

echo "📋 Шаг 1: Проверка текущего состояния..."

# Показываем запущенные контейнеры
echo "Запущенные контейнеры:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "📋 Шаг 2: Остановка и пересборка контейнеров..."

# Останавливаем контейнеры
docker-compose down

# Пересобираем и запускаем
echo "🔨 Пересборка контейнеров..."
docker-compose build --no-cache

echo "🚀 Запуск контейнеров..."
docker-compose up -d

# Ждем немного для инициализации
echo "⏳ Ожидание инициализации контейнеров (30 секунд)..."
sleep 30

echo ""
echo "📋 Шаг 3: Проверка состояния после запуска..."

# Проверяем статус контейнеров
echo "Статус контейнеров PC Configurator:"
docker-compose ps

echo ""
echo "Все контейнеры в сети app_network:"
docker ps --filter "network=app_network" --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "📋 Шаг 4: Проверка сети..."

# Проверяем сеть
if docker network inspect app_network >/dev/null 2>&1; then
    echo "✅ Сеть app_network существует"
    
    # Подключаем контейнеры к сети, если они не подключены
    echo "🔗 Подключение контейнеров к сети app_network..."
    docker network connect app_network pc_configurator_backend 2>/dev/null || echo "Backend уже подключен к сети"
    docker network connect app_network pc_configurator_frontend 2>/dev/null || echo "Frontend уже подключен к сети"
else
    echo "❌ Сеть app_network не существует. Создание сети..."
    docker network create app_network
    docker network connect app_network pc_configurator_backend
    docker network connect app_network pc_configurator_frontend
fi

echo ""
echo "📋 Шаг 5: Перезапуск nginx..."

# Перезапускаем nginx
if docker ps --format "{{.Names}}" | grep -q "events-nginx"; then
    echo "🔄 Перезапуск nginx..."
    docker restart events-nginx
    sleep 5
    echo "✅ Nginx перезапущен"
else
    echo "⚠️ Контейнер events-nginx не найден. Возможно, он называется по-другому."
    echo "Доступные nginx контейнеры:"
    docker ps --format "{{.Names}}" | grep nginx || echo "Nginx контейнеры не найдены"
fi

echo ""
echo "📋 Шаг 6: Финальная проверка..."

# Проверяем логи backend
echo "Последние логи backend:"
docker logs --tail 10 pc_configurator_backend

echo ""
echo "Последние логи frontend:"
docker logs --tail 10 pc_configurator_frontend

echo ""
echo "📋 Шаг 7: Тестирование подключения..."

# Тестируем подключение к backend
echo "🧪 Тестирование backend API..."
if docker exec pc_configurator_backend curl -f http://localhost:8000/health 2>/dev/null; then
    echo "✅ Backend API отвечает"
else
    echo "❌ Backend API не отвечает"
fi

echo ""
echo "🎉 Скрипт завершен!"
echo ""
echo "📝 Следующие шаги:"
echo "1. Проверьте, что все контейнеры запущены: docker ps"
echo "2. Проверьте логи nginx: docker logs events-nginx"
echo "3. Если нужен SSL сертификат, следуйте инструкциям в ssl-setup.md"
echo "4. Проверьте доступность сайта: curl -I http://unl-computers.duckdns.org" 