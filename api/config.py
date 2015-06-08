import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SCRET_KEY = os.environ.get('SECRET_KEY') or 'Hard to guess string'
    DB_URI = "mongodb://localhost" 
    DB_NAME = "oga"
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TEST=True

class ProductionConfig(Config):
    PRODUCTION=True


config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
        }
