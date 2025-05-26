#!/bin/bash

echo "🚀 Исправляем проблемы с развертыванием..."

# 1. Остановить все контейнеры
echo "⏹️ Остановка контейнеров..."
docker-compose down 2>/dev/null || true

# 2. Настройка PostgreSQL
echo "🔧 Настройка PostgreSQL..."

# Проверяем статус PostgreSQL
if ! systemctl is-active --quiet postgresql; then
    echo "❌ PostgreSQL не запущен. Запускаем..."
    sudo systemctl start postgresql
fi

# Настраиваем PostgreSQL для Docker подключений
echo "🔧 Настройка postgresql.conf..."
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf
sudo sed -i "s/listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf

# Настраиваем pg_hba.conf для Docker сети
echo "🔧 Настройка pg_hba.conf..."
if ! grep -q "172.17.0.0/16" /etc/postgresql/*/main/pg_hba.conf; then
    sudo bash -c 'echo "host all all 172.17.0.0/16 md5" >> /etc/postgresql/*/main/pg_hba.conf'
fi

# Перезапускаем PostgreSQL
echo "🔄 Перезапуск PostgreSQL..."
sudo systemctl restart postgresql

# Создаем базы данных
echo "🗄️ Создание баз данных..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" 2>/dev/null || echo "Пароль уже установлен"
sudo -u postgres psql -c "CREATE DATABASE pc_configurator;" 2>/dev/null || echo "База pc_configurator уже существует"
sudo -u postgres psql -c "CREATE DATABASE events_db;" 2>/dev/null || echo "База events_db уже существует"

# 3. Проверка Nginx
echo "🔧 Проверка Nginx..."
if ! systemctl is-active --quiet nginx; then
    echo "❌ Nginx не запущен. Запускаем..."
    sudo systemctl start nginx
fi

# Проверяем конфигурацию Nginx
sudo nginx -t && echo "✅ Nginx конфигурация корректна" || echo "❌ Ошибка в конфигурации Nginx"

# 4. Тестируем подключение к PostgreSQL
echo "🧪 Тест подключения к PostgreSQL..."
if PGPASSWORD=postgres psql -h 172.17.0.1 -U postgres -d postgres -c "SELECT 1;" >/dev/null 2>&1; then
    echo "✅ PostgreSQL доступен из Docker"
else
    echo "❌ PostgreSQL недоступен из Docker"
    echo "Проверяем порты:"
    sudo netstat -tlnp | grep 5432
fi

# 5. Пересборка и запуск контейнеров
echo "🔄 Пересборка контейнеров..."
docker-compose build --no-cache

echo "🚀 Запуск контейнеров..."
docker-compose up -d

# 6. Ждем запуска
echo "⏳ Ждем запуска контейнеров (60 секунд)..."
sleep 60

# 7. Проверка статуса
echo "📊 Статус контейнеров:"
docker-compose ps

# 8. Проверка логов
echo "📋 Логи backend (последние 10 строк):"
docker-compose logs --tail=10 backend

# 9. Тестирование API
echo "🧪 Тестирование API..."
echo "Backend health check:"
curl -f http://localhost:8000/health && echo " ✅" || echo " ❌"

echo "CORS test:"
curl -H "Origin: https://unl-computers.duckdns.org" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/api/v1/components/category/cpu \
     -s -o /dev/null -w "%{http_code}" && echo " ✅ CORS работает" || echo " ❌ CORS не работает"

# 10. Проверка доменов
echo "🌐 Проверка доменов:"
curl -s -o /dev/null -w "%{http_code}" https://unl-computers.duckdns.org && echo "✅ unl-computers.duckdns.org доступен" || echo "❌ unl-computers.duckdns.org недоступен"
curl -s -o /dev/null -w "%{http_code}" https://unl-events.duckdns.org && echo "✅ unl-events.duckdns.org доступен" || echo "❌ unl-events.duckdns.org недоступен"

echo "✅ Исправление завершено!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Проверьте логи: docker-compose logs -f"
echo "2. Откройте сайты:"
echo "   - https://unl-computers.duckdns.org"
echo "   - https://unl-events.duckdns.org"
echo "3. Если проблемы остались, запустите: ./diagnose-issues.sh" 