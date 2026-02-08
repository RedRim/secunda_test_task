#!/bin/bash

if [ ! -f .env ]; then
    cp .env.example .env
else
    echo "Файл .env уже существует"
fi

make up
echo "Ожидание запуска PostgreSQL..."
sleep 5
echo "Применение миграций..."
make migrate
echo "Заполнение БД тестовыми данными..."
make seed
