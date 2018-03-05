import os
from app import make_celery, create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
celery = make_celery(app)
