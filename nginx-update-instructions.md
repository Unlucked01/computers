# 🔧 Обновление Nginx для поддержки двух проектов

## 📋 Что нужно сделать

Вам нужно обновить файл `nginx.conf` в вашем проекте events, чтобы он обслуживал оба домена:
- `unl-events.duckdns.org` (существующий)
- `unl-computers.duckdns.org` (новый)

## 🔄 Обновленная конфигурация Nginx

Замените содержимое вашего `nginx.conf` на следующее:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Логирование
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Основные настройки
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    # Gzip сжатие
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Upstream для Events проекта
    upstream events_backend {
        server events-backend:8000;
    }

    upstream events_frontend {
        server events-frontend:3000;
    }

    # Upstream для PC Configurator проекта
    upstream pc_backend {
        server pc_configurator_backend:8000;
    }

    upstream pc_frontend {
        server pc_configurator_frontend:3000;
    }

    # ==========================================
    # EVENTS PROJECT (unl-events.duckdns.org)
    # ==========================================
    
    # HTTP редирект для events
    server {
        listen 80;
        server_name unl-events.duckdns.org;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS для events
    server {
        listen 443 ssl http2;
        server_name unl-events.duckdns.org;

        ssl_certificate /etc/letsencrypt/live/unl-events.duckdns.org/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/unl-events.duckdns.org/privkey.pem;

        # SSL настройки
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # API для events
        location /api/ {
            proxy_pass http://events_backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Статические файлы для events
        location /static/ {
            proxy_pass http://events_backend/static/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Фронтенд для events
        location / {
            proxy_pass http://events_frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_cache_bypass $http_upgrade;
        }
    }

    # ==========================================
    # PC CONFIGURATOR (unl-computers.duckdns.org)
    # ==========================================
    
    # HTTP редирект для pc configurator
    server {
        listen 80;
        server_name unl-computers.duckdns.org;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS для pc configurator
    server {
        listen 443 ssl http2;
        server_name unl-computers.duckdns.org;

        ssl_certificate /etc/letsencrypt/live/unl-computers.duckdns.org/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/unl-computers.duckdns.org/privkey.pem;

        # SSL настройки
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # API для pc configurator
        location /api/ {
            proxy_pass http://pc_backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Статические файлы для pc configurator
        location /static/ {
            proxy_pass http://pc_backend/static/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Документация API
        location /docs {
            proxy_pass http://pc_backend/docs;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /redoc {
            proxy_pass http://pc_backend/redoc;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Фронтенд для pc configurator
        location / {
            proxy_pass http://pc_frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

## 🗄️ Настройка базы данных

Вам нужно создать новую базу данных для PC Configurator в существующем PostgreSQL:

```bash
# Подключитесь к PostgreSQL контейнеру
docker exec -it events-db psql -U postgres

# Создайте новую базу данных
CREATE DATABASE pc_configurator;

# Выйдите из psql
\q
```

## 🚀 Деплой

1. **Обновите nginx.conf** в проекте events
2. **Создайте базу данных** как показано выше
3. **Получите SSL сертификат** для нового домена:
```bash
# В директории events проекта
docker exec events-nginx certbot certonly --webroot -w /var/www/certbot --email your-email@example.com -d unl-computers.duckdns.org --agree-tos
```

4. **Запустите PC Configurator**:
```bash
# В директории computers проекта
docker-compose up -d
```

5. **Перезапустите Nginx**:
```bash
# В директории events проекта
docker-compose restart nginx
```

## 📊 Проверка

После деплоя проверьте:
- https://unl-events.duckdns.org (должен работать как раньше)
- https://unl-computers.duckdns.org (новый проект)

## 🔧 Архитектура

```
Internet
    ↓
Nginx (events проект) - порты 80/443
    ↓
┌─────────────────┬─────────────────┐
│   Events        │  PC Configurator│
│   Frontend      │   Frontend      │
│   Backend       │   Backend       │
└─────────────────┴─────────────────┘
                      ↓
              Shared PostgreSQL
              (events-db container)
``` 