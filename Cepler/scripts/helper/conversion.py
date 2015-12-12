def getKilogram( startUnit, value):
	if(startUnit == "t"):

		return value/1000;
	elif (startUnit == "g"):
		return value *1000;

def convert( unit, unitName, value):
	if (unit == Mapping.Weight):
		getKilogram(unitName, value)
	pass