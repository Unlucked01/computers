#!/bin/bash

echo "🔧 Исправляем подключение PostgreSQL для Docker..."

# 1. Проверяем статус PostgreSQL
echo "📊 Статус PostgreSQL:"
sudo systemctl status postgresql --no-pager

# 2. Настраиваем PostgreSQL для принятия подключений от Docker
echo "🔧 Настраиваем postgresql.conf..."
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf

# 3. Настраиваем pg_hba.conf для Docker сети
echo "🔧 Настраиваем pg_hba.conf..."
sudo bash -c 'echo "host all all 172.17.0.0/16 md5" >> /etc/postgresql/*/main/pg_hba.conf'

# 4. Перезапускаем PostgreSQL
echo "🔄 Перезапускаем PostgreSQL..."
sudo systemctl restart postgresql

# 5. Проверяем, что PostgreSQL слушает на всех интерфейсах
echo "📡 Проверяем порты:"
sudo netstat -tlnp | grep 5432

# 6. Тестируем подключение
echo "🧪 Тестируем подключение..."
psql -h 172.17.0.1 -U postgres -d postgres -c "SELECT version();" || echo "❌ Подключение не удалось"

# 7. Создаем базу данных если не существует
echo "🗄️ Создаем базы данных..."
sudo -u postgres psql -c "CREATE DATABASE pc_configurator;" 2>/dev/null || echo "База pc_configurator уже существует"
sudo -u postgres psql -c "CREATE DATABASE events_db;" 2>/dev/null || echo "База events_db уже существует"

echo "✅ Настройка завершена!"
echo "🔄 Теперь перезапустите Docker контейнеры:"
echo "   docker-compose down && docker-compose up -d --build" 