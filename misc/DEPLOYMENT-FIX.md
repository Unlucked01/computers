# 🔧 Исправление проблем развертывания

## 🚨 Обнаруженные проблемы:

1. **Events: 502 Bad Gateway** - Nginx не может подключиться к backend
2. **PC Configurator: OPTIONS 400** - проблема с CORS preflight запросами

## ✅ Исправления:

### 1. CORS настройки
- ✅ Обновлен `backend/app/config.py` с правильными доменами
- ✅ Добавлена поддержка переменных окружения для CORS

### 2. PostgreSQL подключение
- ✅ Обновлен `docker-compose.yml` для использования `172.17.0.1`
- ✅ Добавлены `extra_hosts` и `network_mode: bridge`

### 3. API URL в фронтенде
- ✅ Исправлен `frontend/next.config.js` fallback URL

## 🚀 Быстрое исправление:

```bash
# Запустить автоматическое исправление
chmod +x fix-deployment-issues.sh
./fix-deployment-issues.sh
```

## 🔍 Диагностика:

```bash
# Если проблемы остались
chmod +x diagnose-issues.sh
./diagnose-issues.sh
```

## 📋 Ручное исправление:

### PostgreSQL:
```bash
# Настроить PostgreSQL для Docker
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf
sudo bash -c 'echo "host all all 172.17.0.0/16 md5" >> /etc/postgresql/*/main/pg_hba.conf'
sudo systemctl restart postgresql
```

### Контейнеры:
```bash
# Пересобрать и запустить
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Проверка:
```bash
# Тест PostgreSQL
PGPASSWORD=postgres psql -h 172.17.0.1 -U postgres -d postgres -c "SELECT 1;"

# Тест API
curl http://localhost:8000/health

# Тест CORS
curl -H "Origin: https://unl-computers.duckdns.org" -X OPTIONS http://localhost:8000/api/v1/components/category/cpu
```

## 🎯 Ожидаемый результат:

- ✅ **Events**: `https://unl-events.duckdns.org` работает без 502 ошибок
- ✅ **PC Configurator**: `https://unl-computers.duckdns.org` работает без CORS ошибок
- ✅ **API**: Все запросы проходят успешно
- ✅ **PostgreSQL**: Доступен из Docker контейнеров

## 🔧 Основные изменения:

1. **backend/app/config.py**: Добавлены правильные CORS origins
2. **docker-compose.yml**: Исправлено подключение к PostgreSQL
3. **frontend/next.config.js**: Исправлен fallback API URL

После выполнения скрипта оба сайта должны работать корректно! 🚀 