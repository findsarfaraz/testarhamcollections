import os
from testarhamcollections_app.app import make_celery, create_app

app = create_app(os.getenv('FLASK_CONFIG') or None)
celery = make_celery(app)
app.app_context().push()
