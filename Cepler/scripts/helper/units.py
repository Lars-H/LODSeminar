from properties import Mapping
import enum

# convert to base unit
def baseUnit(quantity):
	if quantity == Mapping.COST:
		return MonetaryUnits.DOLLAR.value
	elif quantity == Mapping.DISTANCE:
		return DistanceUnits.METER.value
	elif quantity == Mapping.WEIGHT:
		return MassUnits.KILOGRAM.value

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
	EURO = 'euro'
	DOLLAR = 'usd'

class WikidataUnits:
	wdUnits = { MassUnits.TON.value: "http://www.wikidata.org/entity/Q191118", 
				MassUnits.KILOGRAM.value: "http://www.wikidata.org/entity/Q11570",
				MassUnits.GRAM.value: "http://www.wikidata.org/entity/Q41803",
				DistanceUnits.KILOMETER.value: "http://www.wikidata.org/entity/Q828224",
				DistanceUnits.METER.value: "http://www.wikidata.org/entity/Q11573",
				DistanceUnits.CENTIMETER.value: "http://www.wikidata.org/entity/Q174728",
				MonetaryUnits.EURO.value: "http://www.wikidata.org/entity/Q4916",
				MonetaryUnits.DOLLAR.value: "http://www.wikidata.org/entity/Q4917"
	}