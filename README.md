# Проект «Фудграм» (продуктовый помошник)
доступен по адресу https://foodbigbubam.ddns.net/

## Стек технологий:
* Python 
* Django 
* DjangoRestFramework 
* PostgresSQL 
* Nginx
* Docker, Docker-compose, DockerHub

## Запуск проекта локально:
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
 sudo docker-compose exec backend python manage.py makemigrations &&
docker-compose exec backend python manage.py migrate &&
docker-compose exec backend python manage.py collectstatic --no-input &&
docker-compose exec backend python manage.py data_loading
```


```
docker-compose exec backend python manage.py createsuperuser
```
### Проект готов к работе

Backend проекта выполнил студент 56 когорты Яндекс Практикума  
Fedor Kulabuhov
https://github.com/Fedor-new-Hope
