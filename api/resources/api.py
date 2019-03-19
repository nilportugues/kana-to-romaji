# coding=utf-8

from flask_restplus import Api
from settings import SWAGGER_UI_ENABLED, FLASK_DEBUG

## Swagger documentation
swagger_docs = '/'
if not SWAGGER_UI_ENABLED:
    swagger_docs = False

## API Instance
api = Api(version='1.0',
          title='Japanese to Romaji API',
          description='Converts Kanji, Katakana and Hiragana texts to romanized text.',
          doc=swagger_docs,
          catch_all_404s=True)


