import application as app
import rdflib

rq = app.RequestHandler()
rdfResult = rq.getResponse('1234', 'kg', 'rdf')