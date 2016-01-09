import application as app
import rdflib

rq = app.RequestHandler()
rdfResult = rq.getResource("dbpedia", 1000, "kg", 0.1)
