#!/bin/bash

# Скрипт для установки и настройки PostgreSQL как системного сервиса

echo "🐘 Установка и настройка PostgreSQL..."

# Обновляем пакеты
sudo apt update

# Устанавливаем PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Запускаем и включаем автозапуск
sudo systemctl start postgresql
sudo systemctl enable postgresql

echo "✅ PostgreSQL установлен и запущен"

# Настраиваем пользователя postgres
echo "🔧 Настройка пользователя postgres..."

# Устанавливаем пароль для пользователя postgres
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"

# Создаем базы данных для проектов
echo "📊 Создание баз данных..."

sudo -u postgres createdb events_db
sudo -u postgres createdb pc_configurator

echo "✅ Базы данных созданы:"
echo "  - events_db"
echo "  - pc_configurator"

# Настраиваем доступ
echo "🔐 Настройка доступа..."

# Редактируем pg_hba.conf для разрешения подключений
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf

# Добавляем правило для подключения с паролем
echo "host    all             all             172.16.0.0/12           md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf
echo "host    all             all             10.0.0.0/8              md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf

# Перезапускаем PostgreSQL
sudo systemctl restart postgresql

echo "✅ PostgreSQL настроен!"
echo ""
echo "📋 Информация о подключении:"
echo "  Host: localhost (или IP сервера)"
echo "  Port: 5432"
echo "  User: postgres"
echo "  Password: postgres"
echo "  Databases: events_db, pc_configurator"
echo ""
echo "🧪 Тест подключения:"
echo "  psql -h localhost -U postgres -d events_db" 