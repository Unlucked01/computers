#!/bin/bash

echo "🔗 Подключение PC Configurator к сети Events..."

# Находим сеть events
EVENTS_NETWORK=$(docker network ls --format "{{.Name}}" | grep events | grep app_network)

if [ -z "$EVENTS_NETWORK" ]; then
    echo "❌ Сеть events app_network не найдена."
    echo "Создаем сеть app_network..."
    docker network create app_network
    echo "✅ Сеть app_network создана"
else
    echo "✅ Найдена сеть: $EVENTS_NETWORK"
fi

echo ""
echo "🚀 Запуск PC Configurator..."
docker-compose up -d

echo ""
echo "⏳ Ожидание инициализации (30 секунд)..."
sleep 30

echo ""
echo "📋 Проверка статуса..."
docker-compose ps

echo ""
echo "🔄 Перезапуск nginx..."
docker restart events-nginx 2>/dev/null || echo "Nginx не найден или уже перезапущен"

echo ""
echo "✅ Готово! Проверьте логи nginx: docker logs events-nginx" 