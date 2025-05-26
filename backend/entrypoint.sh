#!/bin/bash

# Выходим при любой ошибке
set -e

echo "Запуск entrypoint скрипта..."

# Ждем готовности PostgreSQL
echo "Ожидание готовности PostgreSQL..."
while ! nc -z "${DATABASE_HOST:-postgres}" "${DATABASE_PORT:-5432}"; do
  echo "PostgreSQL недоступен - ждем..."
  sleep 1
done
echo "PostgreSQL доступен!"

# Проверяем переменные окружения
if [ -z "$DATABASE_URL" ]; then
    echo "Предупреждение: DATABASE_URL не установлен, используется значение по умолчанию"
    export DATABASE_URL="postgresql://postgres:postgres@postgres:5432/pc_configurator"
fi

echo "Подключение к базе: $DATABASE_URL"

# Запускаем миграции Alembic
echo "Запуск миграций Alembic..."
alembic upgrade head

# Проверяем, есть ли данные в таблице component_categories
echo "Проверка наличия начальных данных..."
CATEGORY_COUNT=$(psql "$DATABASE_URL" -t -c "SELECT COUNT(*) FROM component_categories;" 2>/dev/null || echo "0")

if [ "$CATEGORY_COUNT" -eq "0" ]; then
    echo "Начальные данные отсутствуют, загружаем из init.sql..."
    psql "$DATABASE_URL" -f /app/init.sql
    echo "Начальные данные успешно загружены!"
else
    echo "Начальные данные уже присутствуют (найдено $CATEGORY_COUNT категорий), пропускаем инициализацию."
fi

echo "Инициализация базы данных завершена!"
echo "Запуск приложения..."
exec "$@" 