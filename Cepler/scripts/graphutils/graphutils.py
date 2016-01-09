import rdflib
from rdflib.namespace import Namespace, RDF, RDFS, FOAF, NamespaceManager
from rdflib import Graph, BNode, Literal, URIRef

class GraphBuilder:
	# Constructor
	def __init__(self):
		self.g = Graph()

		# Define some namespaces
		self.SPIN = Namespace('http://spinrdf.org/spin#')
		self.SEMS = Namespace('http://semanticscience.org/resource/')
		self.SCHEMA = Namespace('http://schema.org/')
		self.PURLP = Namespace('http://purl.org/net/provenance/types#')
		self.PURLD = Namespace('http://purl.org/dqm-vocabulary/v1/dqm#')
		self.LEMON = Namespace('http://lemon-model.net/lemon#')
		self.WD = Namespace('https://www.wikidata.org/wiki/')
		self.FOAF = Namespace('http://xmlns.com/foaf/0.1/')

		self.g.bind("spin", self.SPIN)
		self.g.bind("sems", self.SEMS)
		self.g.bind("schema", self.SCHEMA)
		self.g.bind("purlp", self.PURLP)
		self.g.bind("purld", self.PURLD)
		self.g.bind("lemon", self.LEMON)
		self.g.bind("wd", self.WD)
		self.g.bind("foaf", self.FOAF)

	# This method builds the request section of the graph
	# and the part of the query section that is connected 
	# to the request section.
	def buildRequestGraph(self, inValue, inUnit_wd):
		self.g.add( (BNode('query'), self.SPIN.query, BNode('request')) )
		self.g.add( (BNode('request'), RDF.type, self.PURLP.Query) )
		self.g.add( (BNode('request'), RDF.value, Literal(float(inValue))) )
		self.g.add( (BNode('request'), self.LEMON.context, URIRef(inUnit_wd)) )

		return self.g

	# This method merges the request graph and the result graph
	# collected from a wrapper to build the final graph which is 
	# returned to the user.
	def mergeWithResultGraph(self, resultGraph):
		for triple in resultGraph:
			self.g.add(triple)
		self.g.add( (BNode('query'), self.SCHEMA.result, BNode('result')) )

		return self.g

	# If the program was queried with a factor, add it to the final graph
	def addFactorToGraph(self, factor):
		self.g.add( (BNode('query'), self.SEMS.SIO_001018, Literal(int(factor))) )
		return self.g

	# This method builds a string which displays results and is passed to the UI.
	def buildOutputString(self, inUnit):
		outStr = ""
		for inValue in self.g.objects(BNode('request'), RDF.value): # should only occur once!
			outStr += str(inValue) + " "
		outStr += inUnit + " are about "
		for factor in self.g.objects(BNode('query'), self.SEMS.SIO_001018): # should only occur once!
			outStr += str(factor) + " "
		for label in self.g.objects(BNode('result'), RDFS.label): # should only occur once!
			try:
				outStr += str(label)
			except UnicodeEncodeError:
				return "Oops! An invalid label was delivered by the datasource. Try again!"
		for rType in self.g.objects(BNode('result'), RDF.type): # should occur 0 or 1 times!
			resultType = rType
		for typeLabel in self.g.objects(resultType, RDFS.label): # should occur 0 or 1 times!
			outStr += ", which is a " + str(typeLabel)
		outStr += "."

		# This is preliminary for the interim presentation:
		for resultUri in self.g.objects(BNode('result'), self.PURLD.hasURI): # should only occur once!
			outStr += "</br> </br> <a target=\"_blank\" href=\"" + str(resultUri) + "\">More information</a>"
		for pic in self.g.objects(BNode('result'), FOAF.depiction): # should occur 0 or 1 times!
			#outStr += "</br> </br> <a target=\"_blank\" href=\"" + str(pic) + "\">Picture</a>"
			outStr += "</br> </br> <img src=\"" + str(pic) + "\" height=\"250\" width=\"250\" ></img>"
			#<img src="smiley.gif" alt="Smiley face" height="42" width="42">
		return outStr
