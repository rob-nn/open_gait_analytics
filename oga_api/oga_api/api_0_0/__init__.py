from flask import Blueprint

main_blueprint = Blueprint('oga_api_0_0', __name__)

from . import views
