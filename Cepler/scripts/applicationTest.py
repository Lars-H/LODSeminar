import application as app
import rdflib

rq = app.RequestHandler()

# You can test here.
# For the Cepler algorithm use:
# rq.getResponse(value, unit, format)
# For one of the interfaces use:
# rq.getResource(datasource, value, unit, range)

rq.getResponse(1000, 'km', 'json')
#rq.getResource('wikidata',1000,'euro',1)