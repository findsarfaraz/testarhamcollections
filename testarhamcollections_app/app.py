import os
from flask import Flask, current_app, render_template
from flask_login import current_user

import config as Config
from common import constants as COMMON_CONSTANTS
from main_app.views import main_app as ma
from main_app.error_handling import page_not_found_404, page_not_found_403, page_not_found_500
from user_management.views import user_management as um, AddressNeed
from product_management.views import product_management as pm
from extensions import db, mail, login_manager, principal, csrf, celery

from user_management.models import User, Userroles, Useraddress
from flask_principal import identity_loaded, RoleNeed, UserNeed, Permission
from celery import Celery

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
    # admin_permission = Permission(RoleNeed('Admin'))
    app.register_error_handler(404, page_not_found_404)
    app.register_error_handler(403, page_not_found_403)
    app.register_error_handler(500, page_not_found_500)
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
    principal.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    celery.init_app(app)
    login_manager.login_view = "user_management.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        role = db.engine.execute('CALL GET_USER_ROLES (%s)', current_user.id)
        # role = Userroles.query.filter_by(role_id=1).all()
        current_user.roles = role
        for role in current_user.roles:
            current_user.userrole = role.role

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.role))

        address = Useraddress.query.filter_by(user_id=current_user.id).all()

        current_user.address = address
        if hasattr(current_user, 'address'):
            identity.provides.add(AddressNeed('list', None))
            identity.provides.add(AddressNeed('create', None))
            for add1 in current_user.address:
                identity.provides.add(AddressNeed('get', unicode(add1.address_id)))
                identity.provides.add(AddressNeed('update', unicode(add1.address_id)))
                identity.provides.add(AddressNeed('delete', unicode(add1.address_id)))


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with current_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
