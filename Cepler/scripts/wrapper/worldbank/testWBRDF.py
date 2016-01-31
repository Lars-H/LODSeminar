from wbWrapper import wbWrapper
import simplejson as json
from StringIO import StringIO
from Properties import Mapping
import random
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
import pprint



wbWrapper1 = wbWrapper();

#print wbWrapper1.getDBPic("<http://dbpedia.org/resource/Equatorial_Guinea>")


rdfResult = wbWrapper1.getResults(Mapping.COST, 194590575, 133343000)

#rdfResult = wbWrapper1.getResults(Mapping.COST, 2, 4) 


if rdfResult is not None:


	#rdfResult.serialize(destination='output.txt', format='turtle')

	for stmt in rdfResult:
		pprint.pprint(stmt)
