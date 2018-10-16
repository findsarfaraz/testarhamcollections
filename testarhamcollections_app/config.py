import os
from datetime import timedelta
from celery.schedules import crontab
from user_management.views import add_together

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Common configurations

    """
    PROJECT = "app"
    DEBUG = False
    # Put any configurations here that are common across all environments
    SECRET_KEY = 'THIS IS BASIS SECRET KEY'


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SECRET_KEY = 'THIS IS DEVELOPMENT SECRET KEY'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:welcome@123@localhost:3306/test_arham'
    # CELERY_IMPORTS = ('user_management.views.add_together', )
    CELERY_RESULT_BACKEND = 'rpc://'
    CELERY_BROKER_URL = 'amqp://rabbitmquser:rabbitmqpassword@localhost:5672/myvhost'
    CELERYBEAT_SCHEDULE = {
        'add-every-30-seconds': {
            'task': 'testarhamcollections_app.user_management.views.run_add_together',
            'schedule': timedelta(seconds=10),
        },
    }

    MAIL_SERVER = 'arhamcollections.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'registration@arhamcollections.com'
    MAIL_PASSWORD = 'welcome@123'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    UPLOAD_FOLDER = '/home/sarfaraz/flaskenv/testarhamcollecions/images'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class DefaultConfig(Config):

    # Statement for enabling the development environment
    DEBUG = True

    # Secret key for signing cookies
    SECRET_KEY = 'development key'


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'live.db')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}


def get_config(MODE):
    SWITCH = {
        'LOCAL': DevelopmentConfig,
        'PRODUCTION': ProductionConfig
    }
    return SWITCH[MODE]
