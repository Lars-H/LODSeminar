import rdflib
from rdflib.namespace import Namespace, RDF, FOAF, NamespaceManager
from rdflib import Graph, BNode, Literal, URIRef

class GraphUtils:
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
	# TODO add factor at the end when a result was definitely found.
	def buildRequestGraph(self, inValue, inUnit_wd, factor):
		self.g.add( (BNode('query'), self.SPIN.query, BNode('request')) )
		self.g.add( (BNode('query'), self.SEMS.SIO_001018, Literal(int(factor))) )
		self.g.add( (BNode('request'), RDF.type, self.PURLP.Query) )
		self.g.add( (BNode('request'), RDF.value, Literal(float(inValue))) )
		# TODO right unit here!
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
