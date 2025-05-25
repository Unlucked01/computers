# Настройка SSL сертификата для unl-computers.duckdns.org

## Проблема
Certbot не установлен в nginx контейнере. Нужно использовать отдельный контейнер.

## Решение

### Вариант 1: Standalone режим (рекомендуется)

```bash
# 1. Остановите nginx временно
docker stop events-nginx

# 2. Получите сертификат с помощью отдельного контейнера certbot
docker run -it --rm --name certbot \
  -v /etc/letsencrypt:/etc/letsencrypt \
  -v /var/www/certbot:/var/www/certbot \
  -p 80:80 \
  certbot/certbot certonly --standalone \
  --email your-email@example.com \
  -d unl-computers.duckdns.org \
  --agree-tos

# 3. Запустите nginx обратно
docker start events-nginx
```

### Вариант 2: Webroot режим (если nginx настроен)

```bash
# Если nginx уже настроен для webroot challenge
docker run -it --rm --name certbot \
  -v /etc/letsencrypt:/etc/letsencrypt \
  -v /var/www/certbot:/var/www/certbot \
  certbot/certbot certonly --webroot \
  -w /var/www/certbot \
  --email your-email@example.com \
  -d unl-computers.duckdns.org \
  --agree-tos
```

### Автоматическое обновление

Добавьте в crontab для автоматического обновления:

```bash
# Добавить в crontab (crontab -e)
0 12 * * * docker run --rm -v /etc/letsencrypt:/etc/letsencrypt -v /var/www/certbot:/var/www/certbot certbot/certbot renew --quiet && docker restart events-nginx
```

## После получения сертификата

1. Убедитесь, что nginx конфигурация обновлена согласно `nginx-update-instructions.md`
2. Перезапустите nginx: `docker restart events-nginx`
3. Проверьте, что сайт доступен по HTTPS 