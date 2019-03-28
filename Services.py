from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self):
        return "Employee GET"

class Tracks(Resource):
    def get(self):
        return "Employee TRUCKS"

class Employees_Name(Resource):
    def get(self, employee_id):
        return "Employees_Name"
        

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')