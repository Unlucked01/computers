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

echo "Запуск приложения..."
exec "$@" 