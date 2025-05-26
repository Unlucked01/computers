# 🚀 Настройка с системными сервисами

## Новая архитектура:

- ✅ **PostgreSQL** - системный сервис Ubuntu
- ✅ **Nginx** - системный сервис Ubuntu  
- ✅ **Backend/Frontend** - Docker контейнеры
- ✅ **PDF генерация** - reportlab (исправлено)

## Быстрая установка:

### Полная автоматическая установка:
```bash
chmod +x setup-server.sh
./setup-server.sh
```

### Пошаговая установка:

1. **PostgreSQL:**
```bash
chmod +x setup-postgres.sh
./setup-postgres.sh
```

2. **Nginx:**
```bash
chmod +x setup-nginx.sh
./setup-nginx.sh
```

3. **Запуск приложения:**
```bash
docker-compose up -d --build
```

4. **SSL сертификаты:**
```bash
chmod +x setup-ssl.sh
./setup-ssl.sh
```

## Преимущества новой архитектуры:

- 🚀 **Производительность** - нет Docker overhead для БД и Nginx
- 🔧 **Простота управления** - systemctl для сервисов
- 🔐 **Безопасность** - системные сервисы более защищены
- 📊 **Мониторинг** - стандартные логи Ubuntu
- 🔄 **Автозапуск** - сервисы запускаются при загрузке системы

## Проверка статуса:

```bash
# Системные сервисы
sudo systemctl status postgresql
sudo systemctl status nginx

# Docker контейнеры
docker-compose ps

# Логи
sudo tail -f /var/log/nginx/error.log
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Управление:

```bash
# Перезапуск сервисов
sudo systemctl restart postgresql
sudo systemctl reload nginx

# Перезапуск приложения
docker-compose restart

# Обновление приложения
docker-compose down
docker-compose up -d --build
```

## Порты:

- **PostgreSQL**: 5432 (системный)
- **Nginx**: 80, 443 (системный)
- **Backend**: 8000 (Docker → Nginx)
- **Frontend**: 3000 (Docker → Nginx)

## Подключения:

- **Backend → PostgreSQL**: `host.docker.internal:5432`
- **Nginx → Backend**: `127.0.0.1:8000`
- **Nginx → Frontend**: `127.0.0.1:3000` 