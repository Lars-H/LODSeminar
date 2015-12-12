import enum

# List of possible input units with their quantity, base unit, and normalization factor.
# 't',Mapping.WEIGHT,'kg',1000
# kg,Mapping.WEIGHT,kg,1
# g,Mapping.WEIGHT,kg,0.001
# # not yet included: mg,Mapping.WEIGHT,kg,0.000001
# # not yet included: ly,m,9460528400000000
# km,Mapping.DISTANCE,m,1000
# m,Mapping.DISTANCE,m,1
# # not yet included: dm,m,0.1
# cm,Mapping.DISTANCE,m,0.01
# # not yet included: mm,m,0.001
# 'Euro',Mapping.COST,'US-Dollar',1.0851
# 'US-Dollar',Mapping.COST,'US-Dollar',1


# List of possible input units
class MassUnits(enum.Enum):
	TON = 't'
	KILOGRAM = 'kg'
	GRAM = 'g'

class DistanceUnits(enum.Enum):
	KILOMETER = 'km'
	METER = 'm'
	CENTIMETER = 'cm'

class MonetaryUnits(enum.Enum):
	EURO = 'Euro'
	DOLLAR = 'US-Dollar'