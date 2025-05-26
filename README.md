# 🖥️ PC Configurator - Веб-конфигуратор персональных компьютеров

> Дипломный проект бакалавра по созданию современного веб-приложения для конфигурирования персональных компьютеров с проверкой совместимости компонентов.

## 📋 Описание проекта

PC Configurator — это современное веб-приложение, которое помогает пользователям собрать оптимальную конфигурацию персонального компьютера. Система автоматически проверяет совместимость выбранных компонентов, отслеживает их наличие и предоставляет интуитивный интерфейс для создания сборок ПК.

### ✨ Ключевые возможности

- 🔧 **Пошаговая сборка ПК** - интуитивный процесс выбора компонентов
- ⚡ **Проверка совместимости** - автоматическая проверка совместимости всех компонентов
- 📦 **Отслеживание наличия** - мониторинг наличия компонентов в реальном времени
- 🎨 **2D визуализация** - интерактивная модель компьютера с подсветкой компонентов
- 🔍 **Продвинутые фильтры** - поиск и фильтрация по множеству параметров
- 💾 **Сохранение конфигураций** - возможность сохранить и поделиться сборкой
- 📄 **Экспорт в PDF** - создание отчетов о конфигурации
- 📱 **Адаптивный дизайн** - поддержка всех устройств

## 🚀 Технологический стек

### Frontend
- **Next.js 14** - React фреймворк с SSR/SSG
- **TypeScript** - статическая типизация
- **Tailwind CSS** - utility-first CSS фреймворк
- **Framer Motion** - анимации и интерактивность
- **React Query** - управление состоянием данных
- **Zustand** - глобальное состояние
- **Lucide React** - иконки
- **Axios** - HTTP клиент

### Backend
- **Python 3.11+** - основной язык разработки
- **FastAPI** - современный веб-фреймворк
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - валидация данных
- **Alembic** - миграции базы данных

### DevOps & Tools
- **Docker** - контейнеризация
- **Git** - система контроля версий
- **ESLint** - статический анализ кода
- **Prettier** - форматирование кода

## 🏗️ Архитектура проекта

```
computers/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # ORM модели
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── routers/        # API маршруты
│   │   ├── services/       # Бизнес-логика
│   │   └── utils/          # Утилиты
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js frontend
│   ├── components/         # React компоненты
│   │   ├── Layout/        # Компоненты макета
│   │   └── Configurator/  # Компоненты конфигуратора
│   ├── pages/             # Страницы Next.js
│   ├── hooks/             # Кастомные хуки
│   ├── lib/               # Утилиты и API клиент
│   ├── types/             # TypeScript типы
│   ├── styles/            # Глобальные стили
│   ├── package.json
│   └── Dockerfile
└── README.md
```

## 🚀 Быстрый запуск

### Предварительные требования

- Docker и Docker Compose
- Git

### Запуск приложения

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd computers
   ```

2. **Запустите приложение:**
   ```bash
   docker-compose up -d
   ```

### Доступ к приложению

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Документация:** http://localhost:8000/docs
- **База данных:** localhost:5433 (postgres/postgres)

## 🏗️ Архитектура

### Backend (FastAPI + PostgreSQL)

- **Порт:** 8000
- **База данных:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Миграции:** Alembic
- **API документация:** Swagger/OpenAPI

### Frontend (Next.js)

- **Порт:** 3000
- **Framework:** Next.js 14
- **Стили:** Tailwind CSS

### База данных

Автоматическая инициализация включает:

1. **Создание таблиц** через Alembic миграции
2. **Заполнение данными** из `backend/init.sql`:
   - 8 категорий компонентов
   - 18+ компонентов (процессоры, материнские платы, память, видеокарты, накопители, БП, корпуса)
   - Информация о наличии компонентов

## 🔧 Разработка

### Структура проекта

```
computers/
├── backend/                 # FastAPI приложение
│   ├── app/                # Основной код приложения
│   ├── alembic/            # Миграции базы данных
│   ├── init.sql            # Начальные данные
│   ├── entrypoint.sh       # Скрипт инициализации
│   └── Dockerfile          # Docker образ backend
├── frontend/               # Next.js приложение
├── docker-compose.yml      # Конфигурация Docker
└── test_setup.sh          # Скрипт тестирования
```

### Команды для разработки

**Остановка сервисов:**
```bash
docker-compose down
```

**Пересборка и запуск:**
```bash
docker-compose up --build -d
```

**Просмотр логов:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Подключение к базе данных:**
```bash
docker-compose exec db psql -U postgres -d pc_configurator
```

### Создание новых миграций

```bash
docker-compose exec backend alembic revision --autogenerate -m "описание изменений"
docker-compose exec backend alembic upgrade head
```

## 📊 API Endpoints

### Категории компонентов
- `GET /api/v1/categories` - Список всех категорий
- `GET /api/v1/categories/{slug}` - Категория по slug

### Компоненты
- `GET /api/v1/components` - Список компонентов с фильтрацией
- `GET /api/v1/components/{id}` - Компонент по ID
- `GET /api/v1/components/category/{category_slug}` - Компоненты категории

### Конфигурации
- `POST /api/v1/configurations` - Создание конфигурации
- `GET /api/v1/configurations/{id}` - Получение конфигурации
- `PUT /api/v1/configurations/{id}` - Обновление конфигурации
- `GET /api/v1/configurations/{id}/pdf` - Экспорт в PDF


## 🔒 Переменные окружения

Основные переменные (настраиваются в `docker-compose.yml`):

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/pc_configurator
JWT_SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## 🐛 Устранение неполадок

### База данных не запускается
```bash
docker-compose down -v  # Удаляет volumes
docker-compose up -d db
```

### Backend не может подключиться к БД
```bash
docker-compose logs backend
docker-compose exec db pg_isready -U postgres
```

### Проблемы с миграциями
```bash
docker-compose exec backend alembic current
docker-compose exec backend alembic history
```

### Очистка и пересоздание
```bash
docker-compose down -v
docker system prune -f
docker-compose up --build -d
```

### 🪟 Проблемы на Windows

**Ошибка "no such file or directory /app/entrypoint.sh":**

Эта проблема возникает из-за различий в окончаниях строк между Windows (CRLF) и Unix (LF). 

**Решение 1 (автоматическое):**
Dockerfile уже содержит команду для автоматической конвертации окончаний строк:
```dockerfile
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh
```

**Решение 2 (настройка Git):**
Файл `.gitattributes` в корне проекта обеспечивает правильную обработку окончаний строк:
```gitattributes
*.sh text eol=lf
```

**Решение 3 (ручное):**
Если проблема все еще возникает, выполните:
```bash
# В Git Bash или WSL
dos2unix backend/entrypoint.sh
# Или используйте sed
sed -i 's/\r$//' backend/entrypoint.sh
```

**Настройка Git для Windows:**
```bash
git config --global core.autocrlf false
git config --global core.eol lf
```

## 📝 Логи и мониторинг

**Просмотр логов в реальном времени:**
```bash
docker-compose logs -f
```

**Health checks:**
- Backend: http://localhost:8000/health
- Database: `docker-compose exec db pg_isready -U postgres`


## 📄 Лицензия

Этот проект создан в рамках дипломной работы. Все права защищены.

## 🏆 Достижения проекта

- ✅ Современная архитектура с разделением frontend/backend
- ✅ Адаптивный интерфейс с поддержкой мобильных устройств
- ✅ Автоматическая проверка совместимости компонентов
- ✅ Интерактивная 2D модель компьютера
- ✅ Система фильтрации и поиска
- ✅ Экспорт конфигураций в PDF
- ✅ Современный стек технологий
- ✅ Полная типизация TypeScript
- ✅ Контейнеризация с Docker

---

**PC Configurator** - создайте свой идеальный компьютер! 🚀 