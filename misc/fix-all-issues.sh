#!/bin/bash

echo "🚀 Исправляем все проблемы с подключением..."

# 1. Остановить контейнеры
echo "⏹️ Остановка контейнеров..."
docker-compose down

# 2. Исправить PostgreSQL конфигурацию
echo "🔧 Настройка PostgreSQL..."

# Проверяем, установлен ли PostgreSQL
if ! systemctl is-active --quiet postgresql; then
    echo "❌ PostgreSQL не запущен. Устанавливаем..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Настраиваем PostgreSQL для Docker
echo "🔧 Настраиваем postgresql.conf..."
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf
sudo sed -i "s/listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf

# Настраиваем pg_hba.conf
echo "🔧 Настраиваем pg_hba.conf..."
if ! grep -q "172.17.0.0/16" /etc/postgresql/*/main/pg_hba.conf; then
    sudo bash -c 'echo "host all all 172.17.0.0/16 md5" >> /etc/postgresql/*/main/pg_hba.conf'
fi

# Перезапускаем PostgreSQL
echo "🔄 Перезапуск PostgreSQL..."
sudo systemctl restart postgresql

# Создаем пользователя и базы данных
echo "🗄️ Настройка баз данных..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" 2>/dev/null || echo "Пароль уже установлен"
sudo -u postgres psql -c "CREATE DATABASE pc_configurator;" 2>/dev/null || echo "База pc_configurator уже существует"
sudo -u postgres psql -c "CREATE DATABASE events_db;" 2>/dev/null || echo "База events_db уже существует"

# 3. Проверяем подключение к PostgreSQL
echo "🧪 Тестируем подключение к PostgreSQL..."
if PGPASSWORD=postgres psql -h 172.17.0.1 -U postgres -d postgres -c "SELECT 1;" >/dev/null 2>&1; then
    echo "✅ PostgreSQL доступен"
else
    echo "❌ PostgreSQL недоступен. Проверьте настройки."
    sudo netstat -tlnp | grep 5432
    exit 1
fi

# 4. Пересобираем и запускаем контейнеры
echo "🔄 Пересборка и запуск контейнеров..."
docker-compose up -d --build

# 5. Ждем запуска контейнеров
echo "⏳ Ждем запуска контейнеров..."
sleep 30

# 6. Проверяем статус
echo "📊 Статус контейнеров:"
docker-compose ps

# 7. Проверяем логи
echo "📋 Логи backend:"
docker-compose logs --tail=10 backend

echo "📋 Логи frontend:"
docker-compose logs --tail=10 frontend

# 8. Тестируем API
echo "🧪 Тестируем API..."
sleep 10
curl -f http://localhost:8000/health && echo "✅ Backend API работает" || echo "❌ Backend API недоступен"

echo "✅ Исправление завершено!"
echo "🌐 Проверьте сайт: https://unl-computers.duckdns.org" 