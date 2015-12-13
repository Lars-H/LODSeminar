from dbpediaWrapper import DBPediaWrapper
import simplejson as json
from StringIO import StringIO
from properties import Mapping
import random
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
import pprint

dpwarpper = DBPediaWrapper();


#Generate Random Division 
orig_value = 45000000
upperBound = orig_value / 1000;
steps = orig_value / 100;
factor = random.randrange(1, upperBound,steps)
if factor == 0:
	factor = 1
value = orig_value  /factor
range = 0.15*value
print(factor)
print(value)


#Get a Result from the Wrapper (RDF Graph)
rdfResult = dpwarpper.getResults(Mapping.WEIGHT, 40000 ,range)
print(rdfResult)

if rdfResult is not None:
	rdfResult.serialize(destination='output.txt', format='turtle')

	for stmt in rdfResult:
		pprint.pprint(stmt)







