from flask import Blueprint

main_blueprint = Blueprint('oga_api_0_0', __name__, url_prefix='/api/v0.0')

from . import views
