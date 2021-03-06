from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from rdflib.namespace import DC, FOAF
from SPARQLWrapper import SPARQLWrapper, N3
import simplejson as json 
import wbProperties
import random
from Properties import Mapping

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
		self.QueryPrefix = "select distinct ?indicator ?actualValue ?indicatorLabel ?countryLabel ?countryDBLink WHERE {"
		self.QuerySuffix = "} LIMIT 100"
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
				results = self.runQuery(queryStr)
			except URLError:
				return None;	
			print(len(results['results']['bindings']))
			#Decode 
			if(len(results['results']['bindings']) >0):
				i  = random.randrange(0, len(results['results']['bindings']), 1)
				
				print i 
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
		#print(len(results))
		return results;

	def buildQuery(self, unit, value, rng):
		#Add the QueryPrefix
		query = self.QueryPrefix

		props = wbProperties.wbIndicators

		#iterate through possible indicators
		for i in range(len(wbProperties.wbIndicators)):
			if(i > 0):
				query += " UNION "
			query += "{ ?indicator <http://purl.org/linked-data/cube#dataSet> <" + wbProperties.wbIndicators[i] + "> . }"

		#limit years
		for i in range(len(wbProperties.wbAllowedYears)):
			if(i > 0):
				query += " UNION "
			query += "{ ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/" + wbProperties.wbAllowedYears[i] + "> . }"

			#retreive acutal values
		query += " ?indicator <http://purl.org/linked-data/sdmx/2009/measure#obsValue> ?actualValue. "

		#retrieve indicator label
		query += " ?indicator <http://worldbank.270a.info/property/indicator> ?TOPindicator. ?TOPindicator <http://www.w3.org/2004/02/skos/core#prefLabel> ?indicatorLabel. "

		#retrieve country label
		query += " ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?country. ?country <http://www.w3.org/2004/02/skos/core#prefLabel> ?countryLabel. "

		#add range
		query += " FILTER (?actualValue > " + str(value - rng/2) + ")"
		query += " FILTER (?actualValue < " + str(value + rng/2) + ")"	

		#retrieve DBpedia Link of country

		query += "OPTIONAL {?country <http://www.w3.org/2002/07/owl#sameAs> ?countryDBLink. FILTER regex(str(?countryDBLink),\"dbpedia\") } "

		
		
		#Add the query Suffix
		query += self.QuerySuffix;
		
		#print query
		return query;


	def resultToRDF(self, result):
		#print(result)
		if(bool(result)):
			indicatorNode = result['indicator']
			indicatorURI = indicatorNode['value']

			indicatorLabelNode = result['indicatorLabel']
			indicatorLabelValue = indicatorLabelNode['value']  

			countryLabelNode = result['countryLabel']
			countryLabelValue = countryLabelNode['value']

			combinedLabelValue = indicatorLabelValue + " of " + countryLabelValue

			indicatorActualValueNode = result['actualValue']
			indicatorActualValue = indicatorActualValueNode['value']

			g = self.__initGraph()

			response = BNode('result');

			g.add( (response, RDFS.label , Literal(combinedLabelValue) ))
			g.add( (response, RDF.value , Literal(indicatorActualValue) )) 
			g.add( (response, self.CEP.unit , self.WD.Q4917))
			g.add( (response, RDF.type , self.CEP.Result))
			g.add( (response, self.CEP.uri , URIRef(indicatorURI)))


			#add picture if existent

			if(result.has_key("countryDBLink")):
				picNode = result['countryDBLink']
				picValue = picNode['value']
				countryDBPic = self.getDBPic(picValue)
				#print countryDBPic
				if countryDBPic is not None:
					g.add( (response, FOAF.depiction, URIRef(countryDBPic) ))
			
			g.serialize(destination='output.txt', format='n3')

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


