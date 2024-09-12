# Обучение FastApi

<!--Установка-->

## Установка через poetry

1.Клонирование репозитория в попку

`git clone https://github.com/AndyRetroWave/Fastapi_training_user.git`

2.Переход в директорию Fastapi_training_user

`cd Fastapi_training_user `

3.Создание виртуального окружения
`poetry install`

4.Активация виртуального окружения
`poetry shell`

5.Создание файла .env или его получение

6.Прогонка миграций алембик
`alembic upgrade head`

7.Запуск приложения
`uvicorn main:app --reload`

## Запуск в докере

1.Клонирование репозитория в попку

`git clone https://github.com/AndyRetroWave/Fastapi_training_user.git`

2.Переход в директорию Fastapi_training_user

`cd Fastapi_training_user `

3.Создание файла .env или его получение

4.Запуск приложения

`docker-compose up --build`
