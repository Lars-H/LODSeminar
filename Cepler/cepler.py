#!/usr/bin/env python
from flask import Flask, jsonify, render_template, request
from scripts.application import RequestHandler


app = Flask(__name__)

@app.route('/getJSON')
def getJSON():
    #Get the variable value and unit
    value = request.args.get('v')
    unit = request.args.get('u')
    key = request.args.get('k')

    if key == "27121571":
        try:
            #Send Request to application
            handler = RequestHandler();
            stringResp = handler.getResponse(value, unit, 'json')
            print(stringResp)
            #Check if request could be answered
            return jsonify(result = str(stringResp))
        except ValueError:   
            print('ERROR: The application has encountered an unexpected Error')  
            return jsonify(result = 'Sorry, we could not process your request! :(')
    else: 
        return jsonify(result = 'Invalid key')

    

@app.route('/getRDF')
def getRDF():
    #Get the variable value and unit
    value = request.args.get('v')
    unit = request.args.get('u')

    #Send Request to application
    #handler = RequestHandler();
    #handler.getResponse(value, unit, 'rdf')

    #Check if request could be answered
    return jsonify(result = 'Here is your RDF data')            

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api')
def api():
    return render_template('api.html')    


if __name__ == '__main__':
    app.debug = True
    app.run()
