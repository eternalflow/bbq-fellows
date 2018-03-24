python manage.py makemigrations
python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

python manage.py loaddata fixtures/products.json
python manage.py runserver 0.0.0.0:8080
