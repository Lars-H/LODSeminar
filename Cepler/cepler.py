#!/usr/bin/env python
import os
from flask import Flask, jsonify, render_template, request, abort, send_from_directory, make_response
from scripts.application import RequestHandler
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from flask_negotiate import consumes, produces


app = Flask(__name__)

#API Methods
@app.route('/compare')
#@produces('text/html')
def compare():
    #Get the Accept Header
    acceptHeader = str(request.accept_mimetypes)

    #Default Response is None
    response = None

    #Get the variable value and unit
    try:
        value = request.args.get('v')
        unit = request.args.get('u')
    except IOError:
        return badRequest("Sorry, one of the parameters was not submitted correctly!");

            

    if not (unit is None) and not(value is None):
        #Send Request to application
        handler = RequestHandler();

        #Check the Accept Header for format

        #JSON-LD
        #Return a JSON-LD response
        if "application/ld+json" in acceptHeader:
            print('Server: Received a JSON-LD request.')
            #Try to get a JSON-LD response
            try:
                response = handler.getResponse(value, unit, 'json-ld')
            except ValueError as e:
                print('Server: A ValueError has occurred. ' + str(e))
                return badRequest("Please specify the parameters correctly!");
            except RuntimeError as e:
                print('Server: A RuntimeError has occurred. ' + str(e))
                return abort(500);    

            #Return answer        
            if not (response is None):
                #Valid response
                #Return it as JSON-LD
                return response;
            else:
                #No result found
                return jsonify(result = 'no result was found');

        #For any other Request a HTML Document is returned          
        else:    
            print('Server: Received a JSON request.')
            try:
                response = handler.getResponse(value, unit, 'json')
                print(response);

            #Handling Value Errors: Input
            except ValueError as e:
                print('Server: A ValueError has occured. ' + str(e))
                return badRequest("Please specify the parameters correctly!");

            #Handling Runtime Errors: Our Server failed somewhere 
            except RuntimeError as e:
                print('Server: A RuntimeError has occured. ' + str(e))
                return abort(500);     
                                      
            if not (response is None):
                #Render template and inject JSON
                return render_template('index_temp.html', data=response)
            else:
                response = " { 'result': 'no result found!', 'in_value' : '" + str (value) + "',  'in_unit' : '" + str(unit)+ "' }";
                return render_template('index_temp.html', data=response)

    else:
        return badRequest("The parameters provided are not valid!");        

#Handling direct negotiation with interfaces
#Example query: http://localhost:5000/dbpedia/compare?v=210&u=t&r=0.2
#
@app.route('/<path:source>/compare')
def compaer_other(source):
    #Get the Accept Header
    acceptHeader = str(request.accept_mimetypes)
    
    #Default Response is none
    response = None;

    #Get the variable value and unit and range
    try:
        value = request.args.get('v')
        print(value)
        unit = request.args.get('u')
        print(unit)
        rng = request.args.get('r')
        print(rng)
    except IOError:
        return badRequest();

    print("Trying to access resource: " + str(source))    

    if not (unit is None) and not(value is None):
        #Send Request to application
        handler = RequestHandler();
    
    #JSON-LD
        if "application/ld+json" in acceptHeader:

            print('Server: Received a JSON-LD request. For DataSource: ' + str(source))
            #Try to get a JSON-LD response
            try:
                response = handler.getResource(str(source), value, unit, rng)
            except ValueError:
                print('Server: A ValueError has occurred.')
                return badRequest('Please specify the parameters correctly!');
            except RuntimeError:
                print('Server: An RuntimeError has occurred.')
                return abort(500);    

            #Return answer        
            if not (response is None):
                #Valid response
                return response;
            else:
                #No result found
                return jsonify(result = 'no result was found');    
        else:
            return abort(406);        
    else:        
        return badRequest(); 


#HTML Pages
@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('index_temp.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api')
def api():
    return render_template('api.html')    

@app.route('/ontology')
def ontology():
    #Get the accept header
    acceptHeader = str(request.accept_mimetypes)

    #When Turtle requested, return turtle, otherwise return HTML
    if "text/turtle" in acceptHeader:
        return send_from_directory('static', 'cepler_ontology.ttl');
    else:
        return render_template('ontology.html')  

@app.route('/download/ontology')
def ontology_download():
    return send_from_directory('static', 'cepler_ontology.ttl');

@app.route('/datasources')
def datasources():
    return render_template('datasources.html')  

@app.route('/describe')
def describe(message ='No Error message!'):
    #Get the variable value and unit
    try:
        value = request.args.get('v')
        unit = request.args.get('u')
    except IOError:
        return badRequest();

    return render_template('index_temp.html', data=data)    


#Return a 400 with a customized message
def badRequest(message ='No Error message!'):
    #Transfer message
    data = message

    #Return message in template
    return render_template('400_temp.html', data = data)


#Main Function
#Starting Server
if __name__ == '__main__':
    app.debug = True
    app.run()
