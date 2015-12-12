#Defining the properties

#Prefixes

wbIndicatorPrefix = "http://worldbank.270a.info/dataset/"

#Indicators
nationalIncome = wbIndicatorPrefix + "NY.ADJ.NNTY.CD"
nationalSavings = wbIndicatorPrefix + "NY.ADJ.NNAT.CD"
weaponExports = wbIndicatorPrefix + "MS.MIL.XPRT.KD"
weaponImports = wbIndicatorPrefix + "MS.MIL.MPRT.KD"
foreignDirectInvestment = wbIndicatorPrefix + "BN.KLT.DINV.CD"
BPI = wbIndicatorPrefix + "NY.GDP.MKTP.CD"
BPIPerCapita = wbIndicatorPrefix + "NY.GDP.PCAP.CD"
governmentHealthExpediturePerCapita = wbIndicatorPrefix + "SH.XPD.PCAP.GX"
minimumWage19yearOld = wbIndicatorPrefix + "DB_mw_19apprentice"
wbIndicators = [nationalIncome, nationalSavings, weaponExports, weaponImports, foreignDirectInvestment, BPI, BPIPerCapita, governmentHealthExpediturePerCapita, minimumWage19yearOld]

#Used years
wbAllowedYears = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]

#---------
#Prefixes
dbo = "http://dbpedia.org/ontology/"
dbp = "http://dbpedia.org/property/"

#Weight Properties
weight = dbo + "weight"
mass = dbo + "mass"
pMass = dbp + "mass"
pWeight = dbp + "weight"
weightProperties = [weight , mass, pMass, pWeight]

#Monetary Properties
#cost = dbo + "cost"
#pCost = dbp +"cost"
pPrice = dbp + "price"
#costProperties = [ pPrice]

#Distance Properties
length = dbo + "length"
distance = dbo + "distance"
height = dbo + "height"
pLength = dbp + "length"
pDistance = dbp + "distance"

distanceProperties = [length, distance,height,  pLength, pDistance]



#Types
#Not used
animal = dbo + "Animal"
person = dbo + "Person"
transportation = dbo + "MeanOfTransportation"

