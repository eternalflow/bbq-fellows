# Description

Simple Django app which allows registered users to throw BBQ Events

# Running application

### Docker
```bash
$ docker-compose up
```

### Manually

```bash
$ python manage.py migrate
$ python manage.py loaddata fixtures/products.json
$ python manage.py runserver 0.0.0.0:80
```

Open localhost in your browser

# Running tests
```bash
$ pytest
```