# Cервис по учёту оборудование на складах

### Описание проекта:
Данное приложение можно использовать в качестве учёта оборудование на складах

Функционал приложение:
- JWT авторизация, аутентификация.
- Регистрация пользователя.
- У аутентифицированных пользователей доступ к API только на уровне чтения, у admin на любой endpoint
- СRUD операции на сущности: Stock, Category, Equipment
- Админ-панель с поиском и фильтрами
- Документация с помощью Swagger

### Инструменты разработки

**Стек:**
- Python >= 3.11
- Django == 5.1
- DRF == 3.15.2
- PostgreSQL == 16.1
- Docker == 20.14.24

## Разработка

##### 1) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 2) Переименовать .env.example на .env (изменить на свои данные, если нужно)

##### 3) Установить docker на свою ОС

    https://docs.docker.com/engine/install/

##### 4) В корневом каталоге проекта(src), создать папку certs и сгенерировать себе ключи (должен быть openssl)

    # Generate an RSA private key, of sizw 2048
    openssl genrsa -out jwt-private.pem 2048

    # Extract the publick key from the key pair, which can be used in a certificate
    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

##### 5) Запустить контейнеры через Makefile (установить make, если нет в системе)
##### Перезапустить контейнер приложение, если не увидел сразу контейнер с БД

    make dev_up

##### 6) Запуск миграции и создание superuser

    make run_migrate
    make create_superuser

##### 7) Перейти в документацию api

    127.0.0.1:8001/api/docs

##### 8) Перейти в админ панель

    127.0.0.1:8001/admin

## Тесты

##### 1) Для запуска теста нужна воспользоваться make

    make run_test
