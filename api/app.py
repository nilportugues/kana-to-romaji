#app.py

import settings

from flask import Flask, Blueprint
from flask_restplus import Swagger
from resources.api import api
from resources.endpoint import ns as to_romaji_resource

## Create the app
app = Flask(__name__)
Swagger(app)

## Init API
blueprint = Blueprint('api', __name__)
api.init_app(blueprint)

# Add Endpoints to API
api.add_namespace(to_romaji_resource)
app.register_blueprint(blueprint)


## Config the app
app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
app.config['SWAGGER_UI_ENABLED'] = settings.SWAGGER_UI_ENABLED

