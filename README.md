# Доска объявлений: расчёт рекомендуемой цены б/у товара

Лабораторная работа: многокомпонентное приложение на Docker Compose.

## Компоненты
- **frontend** — nginx + HTML/JS, порт 8080
- **backend** — Python Flask REST API (CRUD с БД, обращение к web-сервису)
- **db** — PostgreSQL 16, инициализация через `db/init.sql`, данные в volume `pgdata`
- **web-service** — Python Flask микросервис: расчёт рекомендуемой цены б/у товара

## Запуск
    docker compose up -d --build

Открыть: http://localhost:8080

## Остановка
    docker compose down        # данные БД сохраняются
    docker compose down -v     # удалить и данные БД

## Как работает
1. Кнопка «Показать объявления из БД» — frontend -> backend -> PostgreSQL.
2. Кнопка «Рассчитать рекомендуемую цену» — frontend -> backend -> web-service,
   результат сохраняется в БД и показывается в таблице.