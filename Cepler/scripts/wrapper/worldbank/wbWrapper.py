from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from rdflib.namespace import DC, FOAF
from SPARQLWrapper import SPARQLWrapper, N3
import simplejson as json 
import random
import threading
import thread
import time
from Properties import Mapping

#Run Query 
#Used for threading
def runQuery( wrapperO, query ):	
		wrapperO.sparql.setQuery(query);
		results = wrapperO.sparql.query().convert()
		wrapperO.resultCallback(results);


class wbWrapper: 

	#Basic Constructor
	def __init__(self, *args):
		if len(args) > 0:
			self.outformat = str(*args);
		else:
			#JSON as Default
			self.outformat = "json";

		self.endPointUrl = "http://worldbank.270a.info/sparql";
		self.sparql = SPARQLWrapper(self.endPointUrl)
		self.sparql.setReturnFormat(self.outformat)
		self.QueryPrefix = "Prefix wb: <http://worldbank.270a.info/dataset/> Prefix pd: <http://purl.org/linked-data/sdmx/2009/dimension#> Prefix pm: <http://purl.org/linked-data/sdmx/2009/measure#> Prefix y: <http://reference.data.gov.uk/id/year/> select distinct ?i ?actualValue ?indicatorLabel ?countryLabel ?countryDBLink WHERE {"
		self.QuerySuffix = "} LIMIT 70"
		self.__initNamespaces();
		return;

	def __initNamespaces(self):
		#Define Namespaces
		self.CEP = Namespace('http://www.cepler.org/ontology#')
		self.WD = Namespace('https://www.wikidata.org/wiki/')
		
		return;

	#Main function that gets the results
	#@return: RDF Graph	
	def getResults(self, unit, value, rng):
		if unit == Mapping.COST:
			#Build Query String
			queryStr = self.buildQuery(unit, value, rng)
			#Run Query
			try:
				#Old Implementation: No Threading
				#results = self.runQuery(queryStr)

				#Using threading in order to catch timeouts
				self.res = None;
				thread.start_new_thread( runQuery, (self, queryStr))
				timer = 1
				while ((self.res is None) and (timer <= 7) ):
					timer += 1
					time.sleep(1)

				if not (self.res is None):
					results = self.res
					#print("Result found in time.")
					#print(str(results))
				else:
					#print("No result found in time")	
					return None;

			except TypeError:
				return None
			#Decode 
			print len(results['results']['bindings'])
			if(len(results['results']['bindings']) >0):
				i  = random.randrange(0, len(results['results']['bindings']), 1)
				
				try:
					rdfResult = self.resultToRDF(results['results']['bindings'][i])
				except ValueError:	
					rdfResult = None
				#Return Wrapper Result
				return rdfResult;	
			
			else: return None

		else:
			return None ;
		
	#Constructor, defying explicit EndPointUrl
	def setEndpointUrl(self, endPointUrl):
		self.sparql = SPARQLWrapper(self.endPointUrl)
		return;


	def runQuery(self,  query ):		
		self.sparql.setQuery(query);
		results = self.sparql.query().convert()
		return results;

	def resultCallback(self, results):
		self.res = results;


	def buildQuery(self, unit, value, rng):
		#Add the QueryPrefix
		query = self.QueryPrefix

		#limit years
		wbAllowedYears = ["2008", "2009", "2010", "2011", "2012"]
		
		for i in range(len(wbAllowedYears)):
			if(i > 0):
				query += " UNION "
			query += "{ ?i pd:refPeriod y:" + wbAllowedYears[i] + " . }"

			#retreive acutal values
		query += " ?i pm:obsValue ?actualValue. "

		#retrieve indicator label
		query += " ?i <http://worldbank.270a.info/property/indicator> ?Ti. ?Ti <http://www.w3.org/2004/02/skos/core#prefLabel> ?indicatorLabel. "

		#Fliter indicator labels for "current US" (= current US$) as Worldbank does not support currencies as property

		query += " FILTER (regex(str(?indicatorLabel),\"current US\")) FILTER (!regex(str(?indicatorLabel),\"million\"))  "

		#retrieve country label
		query += " ?i pd:refArea ?country. ?country <http://www.w3.org/2004/02/skos/core#prefLabel> ?countryLabel. "

		#add range
		query += " FILTER (?actualValue > " + str(int(value - rng/2)) + ")"
		query += " FILTER (?actualValue < " + str(int(value + rng/2)) + ")"

		#retrieve DBpedia Link of country

		query += "OPTIONAL {?country <http://www.w3.org/2002/07/owl#sameAs> ?countryDBLink. FILTER regex(str(?countryDBLink),\"dbpedia\") } "

		
		
		#Add the query Suffix
		query += self.QuerySuffix;
		print query
		return query;


	def resultToRDF(self, result):
		if(bool(result)):
			indicatorNode = result['i']
			indicatorURI = indicatorNode['value']


			indicatorLabelNode = result['indicatorLabel']
			indicatorLabelValue = indicatorLabelNode['value']  

			countryLabelNode = result['countryLabel']
			countryLabelValue = countryLabelNode['value']

			#year as substring of indicator value
			valueYear = indicatorURI[-4:]
			combinedLabelValue = indicatorLabelValue + " of " + countryLabelValue + " (" + valueYear + ")"

			indicatorActualValueNode = result['actualValue']
			indicatorActualValue = indicatorActualValueNode['value']

			g = self.__initGraph()

			response = BNode('result');

			g.add( (response, RDFS.label , Literal(combinedLabelValue) ))
			g.add( (response, RDF.value , Literal(indicatorActualValue) )) 
			g.add( (response, self.CEP.unit , self.WD.Q4917))
			g.add( (response, self.CEP.entity , URIRef(indicatorURI)))


			#add picture if existent

			if(result.has_key("countryDBLink")):
				picNode = result['countryDBLink']
				picValue = picNode['value']
				countryDBPic = self.getDBPic(picValue)
				if countryDBPic is not None:
					g.add( (response, FOAF.depiction, URIRef(countryDBPic) ))
			
			#g.serialize(destination='output.txt', format='n3')

		return g	

	def __initGraph(self):
	#Initialize Graph
		g = Graph()

		#Bind Namespace to string variable
		g.bind('cep', self.CEP)
		g.bind('wd', self.WD)
		g.bind('foaf', FOAF)
		return g;		

	def getDBPic(self, resourceURL):
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		query =	" select ?countryPic WHERE { <"  + resourceURL + "> <http://xmlns.com/foaf/0.1/depiction> ?countryPic . }"
		sparql.setQuery(query) 
		sparql.setReturnFormat("json")
		queryResult = sparql.query().convert()
		try:
			picResult = queryResult['results']['bindings'][0]
		except IndexError:
			picResult = None
		
		#convert to RDF
		if(bool(picResult)):
			countryNode = picResult['countryPic']
			picURI = countryNode['value']
			return picURI;

		else: return None


