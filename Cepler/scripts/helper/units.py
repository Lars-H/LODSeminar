import enum

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