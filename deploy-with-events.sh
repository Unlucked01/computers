#!/bin/bash

# Скрипт для развертывания PC Configurator с подключением к проекту Events

echo "🚀 Развертывание PC Configurator с подключением к Events..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Убедитесь, что вы в корне проекта PC Configurator."
    exit 1
fi

echo "📋 Шаг 1: Проверка сети Events..."

# Получаем имя сети проекта events
EVENTS_NETWORK=$(docker network ls --format "{{.Name}}" | grep events | head -1)

if [ -z "$EVENTS_NETWORK" ]; then
    echo "❌ Сеть проекта Events не найдена. Убедитесь, что проект Events запущен."
    echo "Доступные сети:"
    docker network ls
    exit 1
else
    echo "✅ Найдена сеть Events: $EVENTS_NETWORK"
fi

echo ""
echo "📋 Шаг 2: Обновление docker-compose.yml..."

# Обновляем docker-compose.yml с правильным именем сети
sed -i.bak "s/events_app_network/$EVENTS_NETWORK/g" docker-compose.yml
echo "✅ Обновлен docker-compose.yml для использования сети: $EVENTS_NETWORK"

echo ""
echo "📋 Шаг 3: Остановка существующих контейнеров..."
docker-compose down

echo ""
echo "📋 Шаг 4: Сборка и запуск контейнеров..."
docker-compose up -d --build

echo ""
echo "📋 Шаг 5: Ожидание инициализации..."
sleep 30

echo ""
echo "📋 Шаг 6: Проверка статуса..."

# Проверяем статус контейнеров
echo "Статус контейнеров PC Configurator:"
docker-compose ps

echo ""
echo "Контейнеры в сети $EVENTS_NETWORK:"
docker network inspect $EVENTS_NETWORK --format '{{range .Containers}}{{.Name}} {{end}}'

echo ""
echo "📋 Шаг 7: Перезапуск nginx..."

# Перезапускаем nginx
NGINX_CONTAINER=$(docker ps --format "{{.Names}}" | grep nginx | head -1)
if [ ! -z "$NGINX_CONTAINER" ]; then
    echo "🔄 Перезапуск $NGINX_CONTAINER..."
    docker restart $NGINX_CONTAINER
    sleep 5
    echo "✅ Nginx перезапущен"
else
    echo "⚠️ Nginx контейнер не найден"
fi

echo ""
echo "📋 Шаг 8: Финальная проверка..."

# Проверяем логи
echo "Последние логи backend:"
docker logs --tail 5 pc_configurator_backend

echo ""
echo "Последние логи frontend:"
docker logs --tail 5 pc_configurator_frontend

echo ""
echo "🎉 Развертывание завершено!"
echo ""
echo "📝 Следующие шаги:"
echo "1. Проверьте логи nginx: docker logs $NGINX_CONTAINER"
echo "2. Убедитесь, что nginx.conf обновлен согласно nginx-update-instructions.md"
echo "3. Получите SSL сертификат согласно ssl-setup.md"
echo "4. Проверьте доступность: curl -I http://unl-computers.duckdns.org"

# Восстанавливаем оригинальный docker-compose.yml
if [ -f "docker-compose.yml.bak" ]; then
    mv docker-compose.yml.bak docker-compose.yml.backup
fi 