#!/bin/bash

echo "🔍 Диагностика проблем с сервисами..."

echo "=== 1. Статус системных сервисов ==="
echo "📊 Nginx:"
sudo systemctl status nginx --no-pager | head -5

echo "📊 PostgreSQL:"
sudo systemctl status postgresql --no-pager | head -5

echo "=== 2. Docker контейнеры ==="
echo "📦 Запущенные контейнеры:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo "=== 3. Проверка портов ==="
echo "🔌 Занятые порты:"
sudo netstat -tlnp | grep -E ":(80|443|5432|8000|8001|3000|3001)\s"

echo "=== 4. Тестирование подключений ==="
echo "🧪 Тест PostgreSQL:"
PGPASSWORD=postgres psql -h 172.17.0.1 -U postgres -d postgres -c "SELECT 1;" 2>/dev/null && echo "✅ PostgreSQL доступен" || echo "❌ PostgreSQL недоступен"

echo "🧪 Тест backend портов:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health && echo " - ✅ PC Configurator backend (8000)" || echo " - ❌ PC Configurator backend (8000)"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health && echo " - ✅ Events backend (8001)" || echo " - ❌ Events backend (8001)"

echo "🧪 Тест frontend портов:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 && echo " - ✅ PC Configurator frontend (3000)" || echo " - ❌ PC Configurator frontend (3000)"
curl -s -o /dev/null -w "%{http_code}" http://localhost:3001 && echo " - ✅ Events frontend (3001)" || echo " - ❌ Events frontend (3001)"

echo "=== 5. Nginx конфигурация ==="
echo "📋 Nginx sites:"
ls -la /etc/nginx/sites-enabled/

echo "📋 Nginx error log (последние 5 строк):"
sudo tail -5 /var/log/nginx/error.log 2>/dev/null || echo "Лог недоступен"

echo "=== 6. Docker логи ==="
echo "📋 PC Configurator backend логи:"
docker logs pc_configurator_backend --tail=5 2>/dev/null || echo "Контейнер не найден"

echo "📋 Events backend логи:"
docker logs events-backend --tail=5 2>/dev/null || echo "Контейнер не найден"

echo "=== 7. CORS проверка ==="
echo "🌐 Тест CORS для PC Configurator:"
curl -H "Origin: https://unl-computers.duckdns.org" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/api/v1/components/category/cpu \
     -v 2>&1 | grep -E "(HTTP|Access-Control|Origin)" || echo "CORS тест не прошел"

echo "✅ Диагностика завершена!" 