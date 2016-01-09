#!/usr/bin/env python
import os
from flask import Flask, jsonify, render_template, request, abort
from scripts.application import RequestHandler
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from flask_negotiate import consumes, produces


app = Flask(__name__)

#API Methods
@app.route('/compare')
#@produces('text/html')
def compare():
    #Get the variable value and unit
    try:
        value = request.args.get('v')
        unit = request.args.get('u')
    except IOError:
        return page_not_found;

    try:
        #Send Request to application
        handler = RequestHandler();
        stringResp = handler.getResponse(value, unit)
        print(stringResp)
        #Check if request could be answered
        return jsonify(result = str(stringResp))
    except ValueError:   
        print('ERROR: The application has encountered an unexpected Error')  
        return jsonify(result = 'no result was found') 

@app.route('/compare')
#@produces('application/json')
def compare_json():
    return page_not_found;


#Handling direct negotiation with interfaces
@app.route('/<path:source>/compare')
def compaer_other(source):
    s = str(source)
    return jsonify(result = 'not implemented yet: ' + str(s));

#HTML Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api')
def api():
    return render_template('api.html')    

@app.route('/ontology')
def ontology():
    return render_template('ontology.html')  


@app.route('/datasources')
def datasources():
    return render_template('datasources.html')      

#Other Function

def page_not_found():
    return abort(404);


if __name__ == '__main__':
    app.debug = True
    app.run()
