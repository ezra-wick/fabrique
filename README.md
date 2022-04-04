# РАССЫЛКИ API
​
Проект для тестового задания, основная задача сервиса управление рассылками и сбор статистики.
​
## Требования
​
Перед запуском работы проверьте наличие 
[Python](https://www.python.org/downloads/),
[Django](https://www.djangoproject.com/), 
[Docker](https://www.docker.com/).
​
## Установка
​
*Клонируйте репозиторий на локальный компьютер. 
Выполните сборку контейнера.*
```
$ docker-compose build
```
​
*Запуск docker-compose.*
```
$ docker-compose up
```
При создании контейнера миграции выполнятся автоматически.
​
## Тестовые данные
​
*fixtures.json - используется для заполнения тестовыми данными.*
```
$ python manage.py loaddata fixtures.json
```
​
## Создание суперпользователя.
```
$ docker-compose run <CONTAINER ID> python manage.py createsuperuser
```
## Выключение контейнера.
```
docker-compose down
```
## Удаление контейнеров.
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

### Документация по API

Перейдите <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Вы увидите автоматическую интерактивную документацию (provided by <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):


![Swagger UI](docs/docs/img/index-swagger-ui.png)