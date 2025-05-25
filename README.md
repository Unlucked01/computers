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

## 🛠️ Установка и запуск

### Предварительные требования

- Node.js 18+ и npm 8+
- Python 3.11+
- PostgreSQL 14+
- Git

### Клонирование репозитория

```bash
git clone <repository-url>
cd computers
```

### Запуск Backend

1. Переход в директорию backend:
```bash
cd backend
```

2. Создание виртуального окружения:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. Установка зависимостей:
```bash
pip install -r requirements.txt
```

4. Настройка базы данных:
```bash
# Создайте базу данных PostgreSQL
# Настройте переменные окружения в .env файле
cp .env.example .env
```

5. Запуск миграций:
```bash
alembic upgrade head
```

6. Запуск сервера:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен по адресу: http://localhost:8000
API документация: http://localhost:8000/docs

### Запуск Frontend

1. Переход в директорию frontend:
```bash
cd frontend
```

2. Установка зависимостей:
```bash
npm install
```

3. Настройка переменных окружения:
```bash
cp .env.example .env.local
```

4. Запуск сервера разработки:
```bash
npm run dev
```

Frontend будет доступен по адресу: http://localhost:3000

## 🐳 Запуск с Docker

### Используя Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка сервисов
docker-compose down
```

### Отдельные контейнеры

Backend:
```bash
cd backend
docker build -t pc-configurator-backend .
docker run -p 8000:8000 pc-configurator-backend
```

Frontend:
```bash
cd frontend
docker build -t pc-configurator-frontend .
docker run -p 3000:3000 pc-configurator-frontend
```

## 📝 API документация

### Основные эндпоинты

- `GET /api/categories` - получение категорий компонентов
- `GET /api/components` - получение списка компонентов с фильтрацией
- `GET /api/components/category/{slug}` - компоненты по категории
- `POST /api/compatibility/check` - проверка совместимости
- `POST /api/configurations` - создание конфигурации
- `GET /api/configurations/{id}/export` - экспорт в PDF

Полная документация доступна по адресу: http://localhost:8000/docs

## 🎨 Дизайн-система

Проект использует собственную дизайн-систему на основе Tailwind CSS:

### Цветовая палитра
- **Primary**: оттенки синего (#3b82f6)
- **Secondary**: оттенки серого (#64748b)
- **Success**: зеленые тона (#22c55e)
- **Warning**: желтые тона (#f59e0b)
- **Error**: красные тона (#ef4444)

### Компоненты
- Кнопки: `.btn-primary`, `.btn-secondary`, `.btn-outline`
- Карточки: `.card`
- Поля ввода: `.input`
- Анимации: `.animate-fade-in`, `.animate-slide-up`

## 🧪 Тестирование

### Frontend
```bash
cd frontend
npm run test
npm run test:coverage
```

### Backend
```bash
cd backend
pytest
pytest --cov=app tests/
```

## 📦 Сборка для продакшена

### Frontend
```bash
cd frontend
npm run build
npm run start
```

### Backend
```bash
cd backend
# Настройка переменных окружения для продакшена
export ENV=production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🚀 Деплой

### Использование Docker

1. Сборка образов:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Запуск в продакшене:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Вклад в проект

Этот проект является дипломной работой. Если у вас есть предложения по улучшению:

1. Создайте Issue для обсуждения изменений
2. Сделайте Fork репозитория
3. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
4. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
5. Отправьте в branch (`git push origin feature/AmazingFeature`)
6. Откройте Pull Request

## 📄 Лицензия

Этот проект создан в рамках дипломной работы. Все права защищены.

## 📞 Контакты

- **Проект**: PC Configurator
- **Статус**: Дипломная работа бакалавра
- **Год**: 2024
- **Специальность**: Информационные системы и технологии

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