# PC Configurator Backend

Backend для конфигуратора ПК на FastAPI с PostgreSQL.

## Особенности

- Автоматическая инициализация базы данных при запуске
- Миграции через Alembic
- Заполнение начальными данными из `init.sql`
- Проверка совместимости компонентов
- Поддержка Docker

## Быстрый запуск

### С Docker Compose (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up --build

# В фоновом режиме
docker-compose up -d --build
```

### Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Установка переменных окружения
cp env.example .env
# Отредактируйте .env под ваши настройки

# Запуск PostgreSQL (например, через Docker)
docker run -d \
  --name postgres-pc \
  -e POSTGRES_DB=pc_configurator \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:15

# Инициализация и запуск
./entrypoint.sh uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DATABASE_URL` | URL подключения к PostgreSQL | `postgresql://postgres:postgres@localhost:5432/pc_configurator` |
| `DATABASE_HOST` | Хост БД | `localhost` |
| `DATABASE_PORT` | Порт БД | `5432` |
| `DATABASE_USER` | Пользователь БД | `postgres` |
| `DATABASE_PASSWORD` | Пароль БД | `postgres` |
| `DATABASE_NAME` | Имя БД | `pc_configurator` |
| `JWT_SECRET_KEY` | Секретный ключ для JWT | `your-secret-key-here` |

## Структура инициализации БД

1. **Проверка готовности PostgreSQL** - ожидаем доступности БД
2. **Проверка существования таблиц** - определяем, нужна ли инициализация
3. **Создание таблиц** - выполняем миграции Alembic (`alembic upgrade head`)
4. **Заполнение данными** - выполняем `init.sql` с начальными данными
5. **Запуск приложения** - стартуем FastAPI сервер

## API

После запуска API будет доступно по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Структура данных

### Основные таблицы:
- `component_categories` - категории компонентов (CPU, GPU, RAM и т.д.)
- `components` - компоненты с характеристиками
- `component_stock` - информация о наличии компонентов
- `component_compatibility` - правила совместимости
- `configurations` - сохраненные конфигурации
- `configuration_items` - компоненты в конфигурациях

## Разработка

### Создание новой миграции

```bash
# Автогенерация миграции
alembic revision --autogenerate -m "описание изменений"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

### Обновление данных

Для обновления начальных данных отредактируйте файл `init.sql`. При следующем запуске с пустой БД данные будут применены автоматически.

## Логи

Entrypoint скрипт выводит подробные логи процесса инициализации:
- Проверка подключения к PostgreSQL
- Статус существования таблиц
- Выполнение миграций
- Загрузка начальных данных
- Запуск приложения

## Troubleshooting

### База данных недоступна
Убедитесь, что PostgreSQL запущен и доступен по указанным в переменных окружения адресу и порту.

### Ошибки миграций
Проверьте целостность файлов миграций в `alembic/versions/` и соответствие моделей SQLAlchemy.

### Дублирование данных
При повторном запуске на существующей БД данные не дублируются благодаря проверке существования таблиц. 