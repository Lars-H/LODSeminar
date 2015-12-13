from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from rdflib.namespace import DC, FOAF
from SPARQLWrapper import SPARQLWrapper, N3
import simplejson as json 
import dbProperties
import random
from properties import Mapping

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
		self.__initNamespaces();
		return;

	def __initNamespaces(self):
		#Define Namespaces
		self.PURLD = Namespace('http://purl.org/dqm-vocabulary/v1/dqm#')
		self.LEMON = Namespace('http://lemon-model.net/lemon#')
		self.WD = Namespace('https://www.wikidata.org/wiki/')
		return;

	#Main function that gets the results
	#@return: RDF Graph	
	def getResults(self, unit, value, rng):
		#Set the global value
		self.unit = unit;

		#Build Query String
		queryStr = self.__buildQuery(unit, value, rng)

		#Run Query
		results = self.__runQuery(queryStr)

		#Decode 
		if(len(results) >0):
			#As of now: Return the first result
			i  = random.randrange(0, len(results), 1)
			try:
				rdfResult = self.__resultToRDF(results['results']['bindings'][i])
			except ValueError:	
				#raise ValueError('Could not parse result to RDF in DBPediaWrapper')
				return None

		#Return Wrapper Result
		return rdfResult;

		#return queryStr;	

	#Constructor, defying explicit EndPointUrl
	def setEndpointUrl(self, endPointUrl):
		self.sparql = SPARQLWrapper(self.endPointUrl)
		return;

	def __runQuery(self,  query ):		
		self.sparql.setQuery(query);
		results = self.sparql.query().convert()
		return results;

	def __buildQuery(self, unit, value, rng):
		#Add the QueryPrefix
		query = self.QueryPrefix

		#Different Properties for different unit
		if unit == Mapping.WEIGHT:
			#Getting Kilograms as input, however in DBP the properties are in gram
			#Therefore dividing
			unit = unit*1000;	

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
			if not (value is None):
				query += " FILTER (?value >" + str(value - rng/2) + ")"
				query += " FILTER (?value <" + str(value + rng/2) + ")"		
		
		#Add the query Suffix
		query += self.QuerySuffix;
	
		#print(query)	
		return query;


	def __resultToRDF(self, result):
		#Check if there is a result
		if(bool(result)):
			#print(result)

			#Get the Uri in uriVale
			uriNode = result['uri']
			uriValue = uriNode['value']

			#Get the label in labeValue
			labelNode = result['label']
			labelValue = labelNode['value']  

			#Get the Actual Value for the Property
			valueNode = result['value']
			valueValue = valueNode['value']

			#Need to retransform the value
			#For Weight
			if self.unit == Mapping.WEIGHT:
				valueValue = float(float(valueValue) / 1000);

			#Initialize Graph
			g = self.__initGraph()

			#Create response Blank Node
			response = BNode('result');

			#Build the Obligatory part for the Response
			g.add( (response, RDFS.label, Literal(labelValue)))	
			g.add( (response, self.PURLD.hasURI, URIRef(uriValue)))
			g.add( (response, RDF.value, Literal(valueValue)))	

			#Defining the context (which is the unit of the response)s
			#Using WikiData in order to have a standardized data source for the unit
			if self.unit == Mapping.WEIGHT:
				g.add( (response, self.LEMON.context, self.WD.Q11570))	
			elif self.unit == Mapping.COST:	
				g.add( (response, self.LEMON.context, self.WD.Q4917))
			elif self.unit == Mapping.DISTANCE:
				g.add( (response, self.LEMON.context, self.WD.Q11573))
			else:
				print("ERROR: Missing unit DBPedia Wrapper")
				return None

			#Add the Optional Part to the response
				
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
		
		#Print Info, when no result found and return None
		else:
			print("INFORMATION: No Result found in DBPedia Wrapper")
			return None

	def __initGraph(self):
		#Initialize Graph
		g = Graph()

		#Bind Namespace to string variable
		g.bind('purld', self.PURLD)
		g.bind('lemon', self.LEMON)
		g.bind('wd', self.WD)
		g.bind('foaf', FOAF)
		return g;		
