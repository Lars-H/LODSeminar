from wrapper.dbpediaWrapper import DBPediaWrapper
import simplejson as json
from StringIO import StringIO
from wrapper.Properties import Mapping
import random
import helper.conversion as con
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
import pprint

class RequestHandler: 	

	def getResponse(self, inValue, inUnit):
		orig_value = float(inValue)
		print("I am handling this request")
		
		dbWrapper = DBPediaWrapper("json");	
		
		factor = random.randrange(1, 100,10)
		newValue = orig_value  /factor
		
		rng = 0.15*newValue;
		print(newValue)
		print(rng)

		#Get a Result from the Wrapper (RDF Graph)
		rdfResult = dbWrapper.getResults(Mapping.WEIGHT, newValue ,rng)

		print(rdfResult)

		return