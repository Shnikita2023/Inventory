DC = docker compose
EXEC = docker exec -it
APP_CONTAINER = web_app_account
DEV_FILES = docker_compose/dev.yaml
ENV = --env-file .env

.PHONY: develop
dev_build:
	${DC} -f ${DEV_FILES} ${ENV} build

.PHONY: develop
dev_up:
	${DC} -f ${DEV_FILES} ${ENV} up -d

.PHONY: develop
dev_down:
		${DC} -f ${DEV_FILES} down --remove-orphans && docker volume prune -f

.PHONE: run_test
run_test:
	${EXEC} ${APP_CONTAINER} sh -c "cd src && pytest -v"

.PHONE: create_superuser
create_superuser:
	${EXEC} ${APP_CONTAINER} sh -c "cd src && python manage.py createsuperuser"

.PHONE: run_migrate
run_migrate:
	${EXEC} ${APP_CONTAINER} sh -c "cd src && python manage.py makemigrations && python manage.py migrate"