#Defining the properties

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
costProperties = [ pPrice]

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

