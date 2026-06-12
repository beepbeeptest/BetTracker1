# 🎯 Bet Tracker — Telegram Mini App

Полноценный трекер ставок прямо в Telegram. Данные каждого пользователя хранятся отдельно на сервере.

## Структура проекта

```
tma-bet/
├── main.py          # FastAPI бэкенд (API + раздача фронтенда)
├── db.py            # SQLite база данных
├── bot.py           # Telegram-бот (открывает Mini App)
├── start.sh         # Запускает бота и сервер вместе
├── requirements.txt
├── Procfile         # Для Railway
└── static/
    └── index.html   # Фронтенд (Mini App)
```

---

## 🚀 Деплой на Railway — пошагово

### Шаг 1 — Получи токен бота
Уже есть ✅

### Шаг 2 — Залей на GitHub
1. Зайди на [github.com](https://github.com) → **New repository**
2. Назови, например, `bet-tracker-tma`
3. Загрузи **все файлы** из этой папки (включая папку `static/`)

> Важно: папка `static` с `index.html` внутри должна быть в корне репозитория

### Шаг 3 — Деплой на Railway
1. Зайди на [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
2. Выбери свой репозиторий
3. Railway сам обнаружит `Procfile` и запустит проект

### Шаг 4 — Добавь переменные окружения
В Railway перейди в свой проект → **Variables** → добавь:

| Переменная | Значение |
|---|---|
| `BOT_TOKEN` | Твой токен от BotFather |
| `APP_URL` | URL твоего приложения (см. ниже) |

**Где взять APP_URL:**
- В Railway перейди в **Settings → Networking → Generate Domain**
- Скопируй URL вида `https://bet-tracker-tma-production.up.railway.app`
- Вставь его в переменную `APP_URL`

### Шаг 5 — Привяжи Mini App к боту
1. Открой **@BotFather** в Telegram
2. Отправь `/newapp` (или `/editapp` если приложение уже есть)
3. Выбери своего бота
4. Укажи `APP_URL` из шага 4 как ссылку на Mini App
5. BotFather выдаст прямую ссылку вида `https://t.me/твойбот/app`

### Шаг 6 — Готово! 🎉
Напиши своему боту `/start` — он пришлёт кнопку открытия трекера.

---

## ⚠️ Важно про хранение данных

На бесплатном Railway файл `bets.db` **сбрасывается при каждом передеплое**.

Чтобы этого избежать, подключи PostgreSQL (бесплатно в Railway):
1. В проекте нажми **New → Database → PostgreSQL**
2. Railway сам добавит переменную `DATABASE_URL`
3. (Опционально) напиши мне — адаптирую `db.py` под PostgreSQL

---

## 🛠 Локальный запуск (для тестирования)

```bash
pip install -r requirements.txt

export BOT_TOKEN="твой_токен"
export APP_URL="http://localhost:8000"

# Запуск сервера
uvicorn main:app --reload

# В другом терминале — бот
python bot.py
```

Открой `http://localhost:8000` в браузере для теста интерфейса.
> Без Telegram initData авторизация не пройдёт — только внутри Telegram.
