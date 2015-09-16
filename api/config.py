import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SCRET_KEY = os.environ.get('SECRET_KEY') or 'Hard to guess string'
    DB_URI = "mongodb://localhost" 
    CSRF_ENABLED=False
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DB_NAME = "oga"
    DEBUG = True

class TestingConfig(Config):
    TESTING=True
    SERVER_NAME = "localhost:5000"
    DB_NAME = "oga_test"

class ProductionConfig(Config):
    DB_NAME = "oga"
    PRODUCTION=True


config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
        }
