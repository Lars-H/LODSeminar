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
		self.QueryPrefix = "select distinct ?indicator ?actualValue ?indicatorLabel ?countryLabel WHERE {"
		self.QuerySuffix = "} LIMIT 100"
		return;

	#Main function that gets the results
	#@return: RDF Graph	
	def getResults(self, unit, value, rng):
		#Build Query String
		queryStr = self.buildQuery(unit, value, rng)
		#Run Query
		results = self.runQuery(queryStr)
		print(len(results))
		#Decode 
		if(len(results) >0):
			i  = random.randrange(0, len(results), 1)
			
			print i 
			try:
				rdfResult = self.resultToRDF(results['results']['bindings'][i])
			except:	
				rdfResult = None

		#Return Wrapper Result
		return rdfResult;


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

		#mMonetary Properties
		if unit == Mapping.COST:
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

			##retrieve country label
			query += " ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?country. ?country <http://www.w3.org/2004/02/skos/core#prefLabel> ?countryLabel. "

			#add range
			query += " FILTER (?actualValue > " + str(value - rng/2) + ")"
			query += " FILTER (?actualValue < " + str(value + rng/2) + ")"	

		else:
			return None ;
		
		#Add the query Suffix
		query += self.QuerySuffix;
		
		print query
		return query;


	def resultToRDF(self, result):
		#print(result)
		if(bool(result)):
			indicatorNode = result['indicator']
			indicatorValue = indicatorNode['value']

			indicatorLabelNode = result['indicatorLabel']
			indicatorLabelValue = indicatorLabelNode['value']  

			countryLabelNode = result['countryLabel']
			countryLabelValue = countryLabelNode['value']

			combinedLabelValue = indicatorLabelValue + " of " + countryLabelValue

			indicatorActualValueNode = result['actualValue']
			indicatorActualValue = indicatorActualValueNode['value']

			g = Graph()

			response = BNode('result1');

#?indicator ?value ?indicatorLabel ?countryLabel

			#g.add( (response, self.PURLD.hasURI, URIRef(uriValue)))
			g.add( (response, RDFS.label , Literal(combinedLabelValue) ))
			g.add( (response, RDF.value , Literal(indicatorActualValue) )) 

			
			g.serialize(destination='output.txt', format='n3')

		return g	
