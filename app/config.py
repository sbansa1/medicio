import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

from environs import Env

env = Env()
env.read_env()

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get( 'DATABASE_URL' ) or \
                               'sqlite:///' + os.path.join(basedir, 'test.db' )
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LEVEL = logging.INFO
    LOGGING_LOCATION = 'error.log'


def create_config_object(env_settings):
    """Creates the new Config Obj"""

    new_config = Config()
    with env.prefixed(env_settings):
        new_config.SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")
        new_config.DEBUG = env.bool('DEBUG',default=False)
        new_config.TESTING = env.bool('TESTING', default=False)

    return new_config






DevelopmentConfig = create_config_object("DEV_")
TestingConfig = create_config_object("TESTING_")
ProductionConfig = create_config_object("PROD_")