from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from rdflib.namespace import DC, FOAF
from SPARQLWrapper import SPARQLWrapper, N3
import simplejson as json 
import dbProperties
from Properties import Mapping

class DBPediaWrapper: 

	#Basic Constructor
	def __init__(self, *args):
		if len(args) > 0:
			self.outformat = str(*args);
		else:
			#JSON as Default
			self.outformat = "json";

		self.endPointUrl = "http://dbpedia.org/sparql";
		self.sparql = SPARQLWrapper(self.endPointUrl)
		self.sparql.setReturnFormat(self.outformat)
		self.QueryPrefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> select distinct ?uri ?value ?label ?type ?typeName ?pic WHERE {"
		self.QuerySuffix = "} LIMIT 100"
		return;

	#Main function that gets the results
	#@return: RDF Graph	
	def getResults(self, unit, value, rng):
		#Build Query String
		queryStr = self.buildQuery(unit, value, rng)

		#Run Query
		results = self.runQuery(queryStr)

		#Decode 
		if(len(results) >0):
			#As of now: Return the first result
			i  = 0
			rdfResult = self.resultToRDF(results['results']['bindings'][i])

		#Return Wrapper Result
		return rdfResult;

		#return queryStr;	

	#Constructor, defying explicit EndPointUrl
	def setEndpointUrl(self, endPointUrl):
		self.sparql = SPARQLWrapper(self.endPointUrl)

		return;


	def runQuery(self,  query ):		
		self.sparql.setQuery(query);
		results = self.sparql.query().convert()
		return results;

	def buildQuery(self, unit, value, rng):
		#Add the QueryPrefix
		query = self.QueryPrefix

		#Different Properties for different unit
		if unit == Mapping.WEIGHT:
			props = dbProperties.weightProperties

			#iterate through possible properties
			for i in range(len(dbProperties.weightProperties)):
				if(i > 0):
					query += " OPTIONAL "

				query += "{ ?uri  <" + dbProperties.weightProperties[i] + "> ?value . }" 



			#Get the label
			query += " ?uri rdfs:label ?label."

			#Get the tyoe and its name (label)
			query += "OPTIONAL { ?uri a ?type. ?type rdfs:label ?typeName. FILTER (lang(?typeName) = 'en')}"
			query += "OPTIONAL { ?uri foaf:depiction ?pic}"
			#Filtering Results
			#Half the range is added, and half subtracted
			if not (value is None):
				query += " FILTER (?value >" + str(value - rng/2) + ")"
				query += " FILTER (?value <" + str(value + rng/2) + ")"	




		#Cost
		elif unit == Mapping.COST:

			for i in range(len(dbProperties.costProperties)):
				if(i > 0):
					query += " OPTIONAL "

				query += "{ ?uri  <" + dbProperties.costProperties[i] + "> ?value . }" 



			#Get the label
			query += " ?uri rdfs:label ?label."

			#Get the tyoe and its name (label)
			query += "OPTIONAL { ?uri a ?type. ?type rdfs:label ?typeName. FILTER (lang(?typeName) = 'en')}"
			query += "OPTIONAL { ?uri foaf:depiction ?pic}"	

			#Filtering Results
			#Half the range is added, and half subtracted
			if not (value is None):
				query += " FILTER (?value >" + str(value - rng/2) + ")"
				query += " FILTER (?value <" + str(value + rng/2) + ")"	



		#Distance
		elif unit == Mapping.DISTANCE:
			for i in range(len(dbProperties.distanceProperties)):
				if(i > 0):
					query += " OPTIONAL "

				query += "{ ?uri  <" + dbProperties.distanceProperties[i] + "> ?value . }" 



			#Get the label
			query += " ?uri rdfs:label ?label."

			#Get the tyoe and its name (label)
			query += "OPTIONAL { ?uri a ?type. ?type rdfs:label ?typeName. FILTER (lang(?typeName) = 'en')}"
			query += "OPTIONAL { ?uri foaf:depiction ?pic}"

		
		#Add the query Suffix
		query += self.QuerySuffix;
	
			
		return query;


	def resultToRDF(self, result):
		#print(result)
		if(bool(result)):
			uriNode = result['uri']
			uriValue = uriNode['value']

			labelNode = result['label']
			labelValue = labelNode['value']  

			g = Graph()

			response = BNode();


			g.add( (URIRef(uriValue) , 	RDF.type , response ))
			g.add( (response, RDFS.label, Literal(labelValue) ))

			if(result.has_key("pic")):
				picNode = result['pic']
				picValue = picNode['value']

				g.add( (response, FOAF.depiction, URIRef(picValue) ))

			if(result.has_key("type")):
				typeNode = result['type']
				typeValue = typeNode['value']

				g.add( (response, RDF.type , URIRef(typeValue) ))	

				if(result.has_key("typeName")):
					typeNameNode = result['typeName']
					typeNameValue = typeNameNode['value']

					g.add( (URIRef(typeValue) , RDFS.label, Literal(typeNameValue)) )

			#g.serialize(destination='output.txt', format='n3')

		return g	
