# 🚀 Быстрое исправление проблем развертывания

## Проблемы, которые были решены:

1. ✅ **Frontend build** - исправлен Dockerfile.prod
2. ✅ **PDF генерация** - заменен weasyprint на reportlab
3. ⚠️ **Сеть Docker** - нужно подключиться к сети events

## Быстрое решение:

### Вариант 1: Автоматический скрипт
```bash
chmod +x connect-to-events.sh
./connect-to-events.sh
```

### Вариант 2: Ручные команды
```bash
# 1. Создать сеть если её нет
docker network create app_network

# 2. Запустить PC Configurator
docker-compose up -d

# 3. Перезапустить nginx
docker restart events-nginx

# 4. Проверить статус
docker-compose ps
docker logs events-nginx
```

## Проверка результата:

```bash
# Проверить, что контейнеры запущены
docker ps | grep pc_configurator

# Проверить сеть
docker network inspect app_network

# Проверить логи
docker logs pc_configurator_backend
docker logs pc_configurator_frontend
docker logs events-nginx
```

## Если всё работает:

1. Обновите nginx.conf согласно `nginx-update-instructions.md`
2. Получите SSL сертификат согласно `ssl-setup.md`
3. Проверьте доступность сайта

## Если проблемы остаются:

1. Проверьте, что проект events запущен
2. Убедитесь, что nginx.conf содержит правильные upstream'ы
3. Проверьте логи всех контейнеров 