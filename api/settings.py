# Flask settings

# Using 127.0.0.1 is important if localhost
# In production it would be intelligent to use the API URL (and no port specified)
FLASK_SERVER_NAME = 'nilportugues.com:5000'
FLASK_DEBUG = False

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = False
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# Swagger
SWAGGER_UI_ENABLED = True

