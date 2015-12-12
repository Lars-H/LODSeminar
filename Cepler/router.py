#!/usr/bin/env python
from flask import Flask, jsonify, render_template, request
from scripts.application import RequestHandler
app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print (request)
    return jsonify(result=a + b)


@app.route('/_get_Response')
def get_Response():

	#Get the variable value and unit
    value = request.args.get('v')
    unit = request.args.get('u')
    print(str(value))
    print(str(unit))
    #Send Request to application
    #handler = RequestHandler();
    #handler.getResponse(value, unit)

    #Check if request could be answered
    return jsonify(result = 'Server is processing the request')


@app.route('/getJSON')
def getJSON():



    return jsonify(result = 'Here is your JSON data')        

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
