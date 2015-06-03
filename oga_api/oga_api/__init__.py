from config import config
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    from .api_0_0 import main_blueprint
    from .web import web_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(web_blueprint)
    return app