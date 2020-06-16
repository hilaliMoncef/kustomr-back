web: gunicorn backend.wsgi
worker: celery worker -A backend -l info
beat: celery beat -A backend -l info