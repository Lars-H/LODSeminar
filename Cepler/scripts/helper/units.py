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
	wdUnits = { MassUnits.TON.value: "https://www.wikidata.org/wiki/Q191118", 
				MassUnits.KILOGRAM.value: "https://www.wikidata.org/wiki/Q11570",
				MassUnits.GRAM.value: "https://www.wikidata.org/wiki/Q41803",
				DistanceUnits.KILOMETER.value: "https://www.wikidata.org/wiki/Q828224",
				DistanceUnits.METER.value: "https://www.wikidata.org/wiki/Q11573",
				DistanceUnits.CENTIMETER.value: "https://www.wikidata.org/wiki/Q174728",
				MonetaryUnits.EURO.value: "https://www.wikidata.org/wiki/Q4916",
				MonetaryUnits.DOLLAR.value: "https://www.wikidata.org/wiki/Q4917"
	}