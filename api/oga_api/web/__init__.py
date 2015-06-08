from flask import Blueprint, render_template, url_for

web_blueprint = Blueprint('oga_api_web', __name__)

from . import views, errors

