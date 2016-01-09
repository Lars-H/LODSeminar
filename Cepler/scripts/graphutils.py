from rdflib import Graph, BNode, Literal, URIRef
from rdflib.namespace import Namespace, RDF, RDFS, FOAF, NamespaceManager
from helper.units import WikidataUnits
import json
import rdflib

class GraphBuilder:

	# Define some namespaces

	#self.LEMON = Namespace('http://lemon-model.net/lemon#')
	#self.PURLD = Namespace('http://purl.org/dqm-vocabulary/v1/dqm#')
	#self.PURLP = Namespace('http://purl.org/net/provenance/types#')
	#self.SCHEMA = Namespace('http://schema.org/')
	#self.SEMS = Namespace('http://semanticscience.org/resource/')
	#self.SPIN = Namespace('http://spinrdf.org/spin#')
	#self.WD = Namespace('https://www.wikidata.org/wiki/')
	CEP = Namespace('http://www.cepler.org/ontology#')
	FOAF = Namespace('http://xmlns.com/foaf/0.1/')

	
	# Constructor
	def __init__(self):
		
		# Create graph
		self.g = Graph()

		# Define prefixes
		#self.g.bind("lemon", self.LEMON)
		#self.g.bind("purld", self.PURLD)
		#self.g.bind("purlp", self.PURLP)
		#self.g.bind("schema", self.SCHEMA)
		#self.g.bind("sems", self.SEMS)
		#self.g.bind("spin", self.SPIN)
		#self.g.bind("wd", self.WD)
		self.g.bind("cep", GraphBuilder.CEP)
		self.g.bind("foaf", GraphBuilder.FOAF)


	# This method builds the request section of the graph
	# and the part of the query section that is connected 
	# to the request section.
	def buildRequestGraph(self, inValue, inUnit_wd):
		
		# Query graph
		self.g.add( (BNode('query'), RDF.type, GraphBuilder.CEP.Query) )
		self.g.add( (BNode('query'), GraphBuilder.CEP.request, BNode('request')) )

		# Request subgraph
		self.g.add( (BNode('request'), RDF.type, GraphBuilder.CEP.Request) )
		self.g.add( (BNode('request'), RDF.value, Literal(float(inValue))) )
		self.g.add( (BNode('request'), GraphBuilder.CEP.unit, URIRef(inUnit_wd)) )

		return self.g

	# This method merges the request graph and the result graph
	# collected from a wrapper to build the final graph which is 
	# returned to the user.
	def mergeWithResultGraph(self, resultGraph):

		# Insert result subgraph
		for triple in resultGraph:
			self.g.add(triple)
		
		# Connect result subgraph to query
		self.g.add( (BNode('query'), GraphBuilder.CEP.result, BNode('result')) )

		return self.g

	# If the program was queried with a factor, add it to the final graph
	def addFactorToGraph(self, factor):

		# Insert factor to query if applicable
		self.g.add( (BNode('query'), GraphBuilder.CEP.factor, Literal(int(factor))) )
		return self.g

	# This method builds a JSON document to pass to the UI.
	def buildJSON(self, factor, inValue, inUnit):

		# Start with a dictionary
		query = {'in_unit': '', 'in_value': '', 'factor': '',
					'result_uri': '', 'result_label': '',
					'out_unit': '', 'out_value': '', 'type_uri': '',
					'type_label': '', 'depiction': ''}
		
		# Those three values are already known, easier than parsing from the graph
		query['factor'] = factor
		query['in_unit'] = inUnit
		query['in_value'] = inValue

		# Those values have to be parsed from the graph:

		# result_uri
		for resultUri in self.g.objects(BNode('result'), GraphBuilder.CEP.uri): # should only occur once!
			query['result_uri'] = resultUri

		# result_label
		for resultLabel in self.g.objects(BNode('result'), RDFS.label): # should only occur once!
			try:
				query['result_label'] = resultLabel
			except UnicodeEncodeError:
				return "Oops! An invalid label was delivered by the datasource. Try again!"

		# out_unit
		for outUnit in self.g.objects(BNode('result'), GraphBuilder.CEP.unit): # should only occur once!
			temp = str(outUnit)

		for key, value in WikidataUnits.wdUnits.iteritems():
			if value == temp: # should also occur exactly once!
				query['out_unit'] = key

		# out_value
		for outValue in self.g.objects(BNode('result'), RDF.value): # should only occur once!
			query['out_value'] = outValue

		# type_uri
		for typeURI in self.g.objects(query['result_uri'], RDF.type): # should occur 0 or 1 times!
			query['type_uri'] = typeURI

		# type_label
		for typeLabel in self.g.objects(query['type_uri'], RDFS.label): # should occur once iff type_uri present!
			query['type_label'] = typeLabel

		# depiction
		for pic in self.g.objects(BNode('result'), FOAF.depiction): # should occur 0 or 1 times!
			query['depiction'] = pic


		jsonarray = json.dumps(query, sort_keys=True, indent=4, separators=(',', ': '))

		return jsonarray



	# This method builds a string which displays results and is passed to the UI.
	# 20160109: deprecated and not used anymore, useful though so keep it temporarily (Nico)
	#def buildOutputString(self, inUnit):
	#	outStr = ""
	#	for inValue in self.g.objects(BNode('request'), RDF.value): # should only occur once!
	#		outStr += str(inValue) + " "
	#	outStr += inUnit + " are about "
	#	for factor in self.g.objects(BNode('query'), self.SEMS.SIO_001018): # should only occur once!
	#		outStr += str(factor) + " "
	#	for label in self.g.objects(BNode('result'), RDFS.label): # should only occur once!
	#		try:
	#			outStr += str(label)
	#		except UnicodeEncodeError:
	#			return "Oops! An invalid label was delivered by the datasource. Try again!"
	#	for rType in self.g.objects(BNode('result'), RDF.type): # should occur 0 or 1 times!
	#		resultType = rType
	#	for typeLabel in self.g.objects(resultType, RDFS.label): # should occur 0 or 1 times!
	#		outStr += ", which is a " + str(typeLabel)
	#	outStr += "."

	#	# This is preliminary for the interim presentation:
	#	for resultUri in self.g.objects(BNode('result'), self.PURLD.hasURI): # should only occur once!
	#		outStr += "</br> </br> <a target=\"_blank\" href=\"" + str(resultUri) + "\">More information</a>"
	#	for pic in self.g.objects(BNode('result'), FOAF.depiction): # should occur 0 or 1 times!
	#		#outStr += "</br> </br> <a target=\"_blank\" href=\"" + str(pic) + "\">Picture</a>"
	#		outStr += "</br> </br> <img src=\"" + str(pic) + "\" height=\"250\" width=\"250\" ></img>"
	#		#<img src="smiley.gif" alt="Smiley face" height="42" width="42">
	#	return outStr