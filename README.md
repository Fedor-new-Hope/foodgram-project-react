# Проект «Фудграм» (продуктовый помошник)
доступен по адресу https://foodbigbubam.ddns.net/

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Fedor-new-Hope/foodgram-project-react.git
```
```
cd foodgram-project-react
```

- Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```
```
source venv/scripts/activate
```

```
python -m pip install --upgrade pip
```

- Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
python manage.py migrate
```

- Запустить проект:

```
python manage.py runserver
```



- Запустите окружение:

* Запустите docker-compose, развёртывание контейнеров выполниться в «фоновом режиме»
```
docker-compose up
```


```
docker-compose exec backend python manage.py makemigrations &&
docker-compose exec backend python manage.py migrate &&
docker-compose exec backend python manage.py collectstatic --no-input &&
docker-compose exec backend python manage.py data_loading
```


```
docker-compose exec backend python manage.py createsuperuser
```
docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --no-input

docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser

docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser

docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations &&

docker compose -f docker-compose.production.yml exec backend python manage.py migrate