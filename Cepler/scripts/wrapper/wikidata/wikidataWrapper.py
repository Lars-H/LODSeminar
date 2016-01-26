from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS , URIRef
from rdflib.namespace import DC, FOAF
from SPARQLWrapper import SPARQLWrapper, N3
import simplejson as json 
import wdProperties
import random
from Properties import Mapping
import httplib

class WikidataWrapper: 

	#Basic Constructor
	def __init__(self, *args):
		if len(args) > 0:
			self.outformat = str(*args);
		else:
			#JSON as Default
			self.outformat = "json";

		self.endPointUrl = "https://query.wikidata.org/bigdata/namespace/wdq/sparql";
		self.sparql = SPARQLWrapper(self.endPointUrl)
		self.sparql.setReturnFormat(self.outformat)
		self.QueryPrefix = "PREFIX schema: <http://schema.org/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX p: <http://www.wikidata.org/prop/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?entity ?entLabel ?entType ?entTypeDescr ?prop ?value WHERE {"
		self.QuerySuffix = "} LIMIT 100"
		self.__initNamespaces();
		self.usefulResultFlag = True 
		return;

	def __initNamespaces(self):
		#Define Namespaces
		self.WD = Namespace('http://www.wikidata.org/entity/')
		self.CEP = Namespace('http://www.cepler.org/ontology#')
		self.P = Namespace('http://www.wikidata.org/prop/')
		self.WIKIBASE = ('http://wikiba.se/ontology#')
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

		#print(len(results['results']['bindings']))
		#Decode 
		if(len(results['results']['bindings']) >0):
			#As of now: Return the first result
			i  = random.randrange(0, len(results['results']['bindings']), 1)
			try:
				rdfResult = self.__resultToRDF(results['results']['bindings'][i])
			except ValueError:	
				#raise ValueError('Could not parse result to RDF in DBPediaWrapper')
				return None

			#Return Wrapper Result
			if (self.usefulResultFlag is True ) :
				return rdfResult;
			else:
				return None
		else: 
			return None
		

	#Constructor, defying explicit EndPointUrl
	def setEndpointUrl(self, endPointUrl):
		self.sparql = SPARQLWrapper(self.endPointUrl)
		return;

	def __runQuery(self,  query ):	
		try:	
			self.sparql.setQuery(query);
			results = self.sparql.query().convert()
		except httplib.HTTPException:
			raise RuntimeError("A timeout occurred when connecting to a datasource.")
				
		return results;

	def __buildQuery(self, unit, value, rng):
		#Add the QueryPrefix
		query = self.QueryPrefix

		#add Value filter

		query += " FILTER (?value >" + str(value - rng/2) + ")"
		query += " FILTER (?value <" + str(value + rng/2) + ")"	

		#weight
		if unit == Mapping.WEIGHT:
			quantUnit = "wd:Q11570" #kg
			excludedProps = [ ] #kilogram
		#cost
		elif unit == Mapping.COST:
			quantUnit = "wd:Q4917"
			excludedProps = [ "p:P710" ]
			#p:P710 = participant

		elif unit == Mapping.DISTANCE:
			quantUnit = "wd:Q11573"  #metre

			excludedProps = [ "p:P2044" ]
			#P2044 = elevation above sea level


		query += "?statement1 wikibase:quantityUnit " + quantUnit + " . ?statement1 wikibase:quantityAmount ?value . ?statement2 ?prop1 ?statement1 . ?entity ?prop ?statement2 .  ?entity rdfs:label ?entLabel  . FILTER (lang(?entLabel)='en') ?entity wdt:P31 ?entType. ?entity schema:description ?entTypeDescr  FILTER (lang(?entTypeDescr)='en')"
		
		#Filter bad Props		
		for i in range(len(excludedProps)):
			query += "FILTER ( ?prop !=" + excludedProps[i] + " ) ."


		#Add the query Suffix
		query += self.QuerySuffix;
	
		return query;


	def __resultToRDF(self, result):
		#Check if there is a result
		if(bool(result)):
			#Get the Uri in uriVale
			entityValue = result['entity']['value']

			#Get the label in labeValue
			propValue = result['prop']['value']  

			#Get the Actual Value for the Property
			valueValue = result['value']['value']

			#get the entity's label
			entityLabelValue = result['entLabel']['value']

			#get entity type
			entityTypeValue = result['entType']['value']

			#get entity type's description
			entityTypeDescriptionValue = result['entTypeDescr']['value']

			#Get: EntityLabel, PropertyLabel, UnitLabel, UnitDescription, UnitDepiction
			furtherInfoResults = self.__getAdditionalInfo(entityValue, propValue)
			if furtherInfoResults is None:
				return None
			
			else:
				#Initialize Graph
				g = self.__initGraph()

				#Create response Blank Node
				fact = BNode('result');

				#Build the Obligatory part for the Response
				#
				
				g.add( (fact, self.CEP.entity, URIRef(entityValue)))
				g.add( (fact, RDF.value, Literal(valueValue)))	
				g.add( (URIRef(entityValue), RDF.type , URIRef(entityTypeValue) ))
				g.add( (URIRef(entityTypeValue) , RDFS.label, Literal(entityTypeDescriptionValue)) )

				#Defining the context (which is the unit of the response)s
				#Using WikiData in order to have a standardized data source for the unit
				if self.unit == Mapping.WEIGHT:
					g.add( (fact, self.CEP.unit, self.WD.Q11570))	
				elif self.unit == Mapping.COST:	
					g.add( (fact, self.CEP.unit, self.WD.Q4917))
				elif self.unit == Mapping.DISTANCE:
					g.add( (fact, self.CEP.unit, self.WD.Q11573))
				else:
					print("ERROR: Missing unit")
					return None

				# Label, if no info avalible, flag result as not useful

				propLabelValue = furtherInfoResults['propLabel']['value']

				factLabel = propLabelValue + " of " + entityLabelValue

				g.add( (fact, RDFS.label, Literal(factLabel)) )

				#add Pic
				if(furtherInfoResults.has_key("pic")):
					picValue = furtherInfoResults['pic']['value']

					g.add( ( fact, FOAF.depiction, URIRef(picValue) ))

				#g.serialize(destination='output.txt', format='n3')
				return g	
			
			#Print Info, when no result found and return None
		else:
			print("INFORMATION: No Result found in WikiData Wrapper")
			return None

	def __initGraph(self):
		#Initialize Graph
		g = Graph()

		#Bind Namespace to string variable
		g.bind('cep', self.CEP)
		g.bind('wd', self.WD)
		g.bind('foaf', FOAF)
		return g;

	def __getAdditionalInfo( self, entityUri, propUri):

		#schon da: ?entity ?entLabel ?entType ?entTypeDescr ?prop ?value

		additionalSparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
		
		additionalSparqlInfoQuery = "PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?propLabel ?pic WHERE{ "

		wikidataEntity = self.__getWikiDataResource(entityUri)
		wikidataProp = self.__getWikiDataResource(propUri)


		#SPARQL Property Label
		additionalSparqlInfoQuery += "wd:" + wikidataProp +" rdfs:label ?propLabel  . FILTER(lang(?propLabel)='en') "

		#SPARQL optional picture
		additionalSparqlInfoQuery += "OPTIONAL {wd:" + wikidataEntity + " wdt:P18 ?pic} "

		#Suffix
		additionalSparqlInfoQuery += "} LIMIT 1"

		additionalSparql.setQuery(additionalSparqlInfoQuery)
		additionalSparql.setReturnFormat("json")
		results = additionalSparql.query().convert()

		if(len(results['results']['bindings']) > 0):

			return results['results']['bindings'][0]
		else: 
			print("INFORMATION: Relevant additional info missing, return null")
			return None

	def __getWikiDataResource( self, uri) :

		#split uri
		splitUri = uri.split("/")
		#select last bit of split URL
		resource = splitUri[len(splitUri)-1]
		return resource


