from logging.handlers import RotatingFileHandler

from flask import Flask

from app.blueprints.users import user
from app.config import TestingConfig, DevelopmentConfig, Config
from app.extensions import db,migrate,login_manager


def create_app(config_settings=Config):

    app = Flask(__name__, instance_relative_config='')
    app.config.from_object(config_settings)
    handler = RotatingFileHandler(app.config.get('LOGGING_LOCATION'), maxBytes=10240,backupCount=10 )
    handler.setLevel(app.config.get('LOGGING_LEVEL'))
    formatter = handler.setFormatter(app.config.get('LOGGING_FORMAT'))
    handler.setFormatter(formatter)

    app.register_blueprint(user)

    app.logger.addHandler(handler)

    error(app)
    extensions(app)


    return app



def extensions(app):

    with app.test_request_context():
        login_manager.init_app(app)
        db.init_app(app)
        migrate.init_app(app,db)



def error(app):
    """"""
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handles the 500 Error"""

        app.logger.error('Server Error: %s', (error))

    @app.errorhandler(404)
    def file_not_found(error):

        app.logger.error('Page Not Found: %s', (error))






