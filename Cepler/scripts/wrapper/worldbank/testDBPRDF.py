from dbpediaWrapper import DBPediaWrapper
import simplejson as json
from StringIO import StringIO
from Properties import Mapping
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
rdfResult = dpwarpper.getResults(Mapping.WEIGHT, value ,range)

if rdfResult is not None:
	#rdfResult.add()
	result = BNode('result1')


	rdfResult.add( (result, RDF.value , Literal(orig_value) ))
	rdfResult.add( (result, URIRef("http://www.w3.org/ns/org#hasUnit") , URIRef("http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Kilogram") ))
	rdfResult.add( (result, URIRef("http://dbpedia.org/ontology/ratio"), Literal(factor) ))

	rdfResult.serialize(destination='output.txt', format='turtle')

	for stmt in rdfResult:
		pprint.pprint(stmt)







