#!/bin/bash

# Скрипт для установки certbot и получения SSL сертификатов

echo "🔐 Установка Certbot и получение SSL сертификатов..."

# Устанавливаем certbot
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

echo "✅ Certbot установлен"

# Получаем сертификат для unl-computers.duckdns.org
echo "📜 Получение сертификата для unl-computers.duckdns.org..."

sudo certbot --nginx -d unl-computers.duckdns.org --non-interactive --agree-tos --email your-email@example.com

if [ $? -eq 0 ]; then
    echo "✅ SSL сертификат для unl-computers.duckdns.org получен!"
else
    echo "❌ Ошибка получения SSL сертификата для unl-computers.duckdns.org"
fi

# Получаем сертификат для unl-events.duckdns.org (если нужно)
echo "📜 Получение сертификата для unl-events.duckdns.org..."

sudo certbot --nginx -d unl-events.duckdns.org --non-interactive --agree-tos --email your-email@example.com

if [ $? -eq 0 ]; then
    echo "✅ SSL сертификат для unl-events.duckdns.org получен!"
else
    echo "❌ Ошибка получения SSL сертификата для unl-events.duckdns.org"
fi

# Настраиваем автоматическое обновление
echo "🔄 Настройка автоматического обновления сертификатов..."

# Добавляем задачу в crontab
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet && systemctl reload nginx") | crontab -

echo "✅ Автоматическое обновление настроено"

# Проверяем статус сертификатов
echo ""
echo "📋 Статус сертификатов:"
sudo certbot certificates

echo ""
echo "🎉 SSL сертификаты настроены!"
echo "Автоматическое обновление будет происходить каждый день в 12:00" 