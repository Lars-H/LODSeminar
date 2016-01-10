from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://worldbank.270a.info/sparql")
sparql.setQuery('    select  ?indicator  WHERE {{ ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/NY.ADJ.NNTY.CD> . } UNION { ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/NY.ADJ.NNAT.CD> . } UNION { ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/MS.MIL.XPRT.KD> . } UNION { ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/MS.MIL.MPRT.KD> . } UNION { ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/BN.KLT.DINV.CD> . } UNION { ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/NY.GDP.MKTP.CD> . } UNION { ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/NY.GDP.PCAP.CD> . } UNION { ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/SH.XPD.PCAP.GX> . } UNION { ?indicator <http://purl.org/linked-data/cube#dataSet> <http://worldbank.270a.info/dataset/DB_mw_19apprentice> . }{ ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2008> . } UNION { ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2009> . } UNION { ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2010> . } UNION { ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2011> . } UNION { ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2012> . } UNION { ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2013> . } UNION { ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2014> . } UNION { ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2015> . } ?indicator <http://purl.org/linked-data/sdmx/2009/measure#obsValue> ?actualValue.  ?indicator <http://worldbank.270a.info/property/indicator> ?TOPindicator. ?TOPindicator <http://www.w3.org/2004/02/skos/core#prefLabel> ?indicatorLabel.  ?indicator <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?country. ?country <http://www.w3.org/2004/02/skos/core#prefLabel> ?countryLabel.  FILTER (?actualValue > 130477) FILTER (?actualValue < 330477)} LIMIT 100')
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["indicator"]["value"])