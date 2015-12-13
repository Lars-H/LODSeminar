import application as app
import rdflib

rq = app.RequestHandler()
rdfResult = rq.getResponse('100000', 'km', 'rdf')