from wikidataWrapper import WikidataWrapper
import simplejson as json
from StringIO import StringIO
from Properties import Mapping
import random
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
import pprint

wikiwrapper = WikidataWrapper();


#Get a Result from the Wrapper (RDF Graph)
#rdfResult = wikiwrapper.getResults(Mapping.DISTANCE, 400000 ,10000)
rdfResult = wikiwrapper.getResults(Mapping.DISTANCE, 5000800, 10003000);



#if rdfResult is not None:
#	rdfResult.serialize(destination='output.txt', format='turtle')

#	for stmt in rdfResult:
#		pprint.pprint(stmt)







