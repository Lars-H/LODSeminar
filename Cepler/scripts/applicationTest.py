import application as app
import rdflib

rq = app.RequestHandler()

# You can test here.
# For the Cepler algorithm use:
# rq.getResponse(value, unit)
# For one of the interfaces use:
# rq.getResource(datasource, value, unit, range)

#print(rq.getResponse(1000, 'kg'))
print(rq.getResource('dbpedia',1000,'kg',50))