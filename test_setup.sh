#!/bin/bash

echo "🚀 Тестирование настройки конфигуратора ПК..."

# Проверяем, что docker-compose работает
echo "📋 Проверка docker-compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose не найден!"
    exit 1
fi

# Останавливаем существующие контейнеры
echo "🛑 Остановка существующих контейнеров..."
docker-compose down -v

# Запускаем сервисы
echo "🔄 Запуск сервисов..."
docker-compose up -d

# Ждем готовности базы данных
echo "⏳ Ожидание готовности базы данных..."
timeout=60
counter=0
while [ $counter -lt $timeout ]; do
    if docker-compose exec -T db pg_isready -U postgres -d pc_configurator > /dev/null 2>&1; then
        echo "✅ База данных готова!"
        break
    fi
    echo "⏳ Ждем базу данных... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

if [ $counter -ge $timeout ]; then
    echo "❌ Таймаут ожидания базы данных!"
    docker-compose logs db
    exit 1
fi

# Ждем готовности backend
echo "⏳ Ожидание готовности backend..."
timeout=120
counter=0
while [ $counter -lt $timeout ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend готов!"
        break
    fi
    echo "⏳ Ждем backend... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

if [ $counter -ge $timeout ]; then
    echo "❌ Таймаут ожидания backend!"
    docker-compose logs backend
    exit 1
fi

# Проверяем API endpoints
echo "🔍 Тестирование API endpoints..."

# Проверяем health endpoint
echo "📊 Проверка /health..."
health_response=$(curl -s http://localhost:8000/health)
if echo "$health_response" | grep -q "ok"; then
    echo "✅ Health check прошел успешно"
else
    echo "❌ Health check не прошел: $health_response"
fi

# Проверяем категории
echo "📂 Проверка /api/v1/categories..."
categories_response=$(curl -s http://localhost:8000/api/v1/categories)
if echo "$categories_response" | grep -q "Процессоры"; then
    echo "✅ Категории загружены успешно"
    category_count=$(echo "$categories_response" | grep -o '"name"' | wc -l)
    echo "📊 Найдено категорий: $category_count"
else
    echo "❌ Категории не найдены: $categories_response"
fi

# Проверяем компоненты
echo "🔧 Проверка /api/v1/components..."
components_response=$(curl -s "http://localhost:8000/api/v1/components?limit=5")
if echo "$components_response" | grep -q "Intel\|AMD"; then
    echo "✅ Компоненты загружены успешно"
    component_count=$(echo "$components_response" | grep -o '"name"' | wc -l)
    echo "📊 Найдено компонентов (первые 5): $component_count"
else
    echo "❌ Компоненты не найдены: $components_response"
fi

# Проверяем базу данных напрямую
echo "🗄️ Проверка данных в базе..."
db_categories=$(docker-compose exec -T db psql -U postgres -d pc_configurator -t -c "SELECT COUNT(*) FROM component_categories;" | tr -d ' ')
db_components=$(docker-compose exec -T db psql -U postgres -d pc_configurator -t -c "SELECT COUNT(*) FROM components;" | tr -d ' ')
db_stock=$(docker-compose exec -T db psql -U postgres -d pc_configurator -t -c "SELECT COUNT(*) FROM component_stock;" | tr -d ' ')

echo "📊 Статистика базы данных:"
echo "   - Категории: $db_categories"
echo "   - Компоненты: $db_components"
echo "   - Записи о наличии: $db_stock"

if [ "$db_categories" -gt 0 ] && [ "$db_components" -gt 0 ] && [ "$db_stock" -gt 0 ]; then
    echo "✅ Все данные успешно загружены в базу!"
else
    echo "❌ Проблема с данными в базе!"
fi

# Показываем логи для диагностики
echo "📋 Последние логи backend:"
docker-compose logs --tail=10 backend

echo ""
echo "🎉 Тестирование завершено!"
echo "🌐 API доступно по адресу: http://localhost:8000"
echo "📚 Документация API: http://localhost:8000/docs"
echo "🔍 Для остановки: docker-compose down" 