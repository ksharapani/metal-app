release: python manage.py migrate
web: gunicorn metal_app.wsgi:application --log-file - --log-level debug