# coding=utf-8

from flask import request
from flask_restplus import Resource, Api, fields
from .api import api
from services.japaneseToRomaji import JapaneseToRomaji

## Resource definition
ns = api.namespace('')

## Resource description
resource_request = api.model('Request', {
    'data': fields.String(description='Japanese text'),
})


@ns.route('/to-romaji')
class ToRomajiResource(Resource):

   @api.expect(resource_request)
   @api.response(200, 'Success')
   @api.response(400, 'Bad Request')
   @api.response(500, 'Internal Server Error')
   def post(self):
    """
    Converts Kanji, Katakana and Hiragana texts to romanized text
    """
    converter = JapaneseToRomaji()
    json = request.json
    input = json['data']
    output = converter.convert(input)

    return output, 200


