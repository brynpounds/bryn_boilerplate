"""Compiled by Bryn Pounds as a 'boilerplate' docker container, swagger 'open API' 2.0 spec,
with a Flask API.

This comes from a project written by Keith Baldwin and Bryn Pounds.
"""
try:
    from flask import Flask
    from flask_restful import Resource, Api
    from apispec import APISpec
    from marshmallow import Schema, fields
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_apispec.extension import FlaskApiSpec
    from flask_apispec.views import MethodResource
    from flask_apispec import marshal_with, doc, use_kwargs
    import requests
    import json
    import time
    import urllib3
    import utils
    
    from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
    from requests.auth import HTTPBasicAuth  # for Basic Auth  
    
    print("All imports are ok............")
except Exception as e:
    print("Error: {} ".format(e))

    
class WeatherControllerSchema(Schema):
    ########  My goto example to verify things are working.  Go grab the weather based on a zip US code.
    ########  For an example, we want swagger to show 2 inputs required for this function.  Could have used Integer, but went with strings for simplicity of example.
    zip = fields.String(required=True, description="zip code",example='66085')
    city = fields.String(required=False, description="city name",example='Overland Park')

class WeatherController(MethodResource, Resource):
    ########  Now just write your code using the 2 inputs.
    import json
    import requests
    ########  Tags is how you group things in swagger.  decription is the label for the specific function.
    @doc(description='Verification things are working with weather test', tags=['Health and testing Endpoints'])
    @use_kwargs(WeatherControllerSchema, location=('json'))
    def post(self, **kwargs):
        #url = """http://192.241.187.136/data/2.5/weather?zip=10001,us&appid=11a1aac6bc7d01ea13f0d2a8e78c227e"""
        ######## insert some default values for ease of testing or demoing.
        url = """http://192.241.187.136/data/2.5/weather?zip=""" + str(kwargs.get("zip", "10001")) + """,us&appid=11a1aac6bc7d01ea13f0d2a8e78c227e"""
        my_response = requests.get(url)
        our_response_content = my_response.content.decode('utf8')
        proper_json_response = json.loads(our_response_content)
        
        _message = kwargs.get("zip", "10001")
        _message2 = kwargs.get("city", "Overland Park")
        #response = {"message":"Weather JSON response for zip code:" + str(_message) + "\n\n" + str(proper_json_response) + "\n\n" + url + _message2}
        response = proper_json_response
        return response
 
