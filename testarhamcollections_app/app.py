import os
from flask import Flask

import config as Config
from common import constants as COMMON_CONSTANTS
from main_app.views import main_app as ma
from user_management.views import user_management as um
from product_management.views import product_management as pm
from extensions import db, mail, login_manager

from user_management.models import User


__all__ = ['create_app']

DEFAULT_BLUEPRINTS = [
    ma, um, pm
]


def create_app(config=None, app_name=None, blueprints=None):
    if app_name is None:
        app_name = Config.DevelopmentConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_path=COMMON_CONSTANTS.INSTANCE_FOLDER_PATH, instance_relative_config=True)

    configure_app(app, config)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    return app


def configure_app(app, config=None):

    app.config.from_object(Config.DevelopmentConfig)

    if config:
        app.config.from_object(config)
    return

    application_mode = os.getenv('APPLICATION_MODE', 'LOCAL')
    app.config.from_object(Config.get_config(application_mode))


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_extensions(app):
    #   pass
    db.init_app(app)

    mail.init_app(app)

    login_manager.init_app(app)
    print "LOGIN MANAGER EXECUTED1"

    @login_manager.user_loader
    def load_user(user_id):
        print "LOGIN MANAGER EXECUTED"
        return User.query.get(int(user_id))



