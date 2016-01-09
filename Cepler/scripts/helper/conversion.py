from properties import Mapping
from units import MassUnits, DistanceUnits, MonetaryUnits
import sys

class Conversions:

	def convert(self, orig_value, orig_unit, quantity):
		norm_value = None
		if (quantity == Mapping.WEIGHT):
			norm_value = self.convertToKilogram(orig_value, orig_unit)
		elif (quantity == Mapping.DISTANCE):
			norm_value = self.convertToMeter(orig_value, orig_unit)
		elif (quantity == Mapping.COST):
			norm_value = self.convertToDollar(orig_value, orig_unit)
		else:
			sys.exit('ERROR: Conversion failed because quantity was not properly set.')
	
		return norm_value
	
	def convertToKilogram(self, orig_value, orig_unit):
		orig_value_parsed = float(orig_value)
		norm_value = None
		if orig_unit == MassUnits.TON.value:
			norm_value = 1000*orig_value
		elif orig_unit == MassUnits.KILOGRAM.value:
			norm_value = orig_value
		elif orig_unit == MassUnits.GRAM.value:
			norm_value = orig_value/1000
		else:
			sys.exit('ERROR: Conversion to kilogram failed.')

		print("Value converted to base unit kilogram: " + str(norm_value))
		return norm_value

	def convertToMeter(self, orig_value, orig_unit):
		orig_value_parsed = float(orig_value)
		norm_value = None
		if orig_unit == DistanceUnits.KILOMETER.value:
			norm_value = 1000*orig_value
		elif orig_unit == DistanceUnits.METER.value:
			norm_value = orig_value
		elif orig_unit == DistanceUnits.CENTIMETER.value:
			norm_value = orig_value/100
		else:
			sys.exit('ERROR: Conversion to meter failed.')

		print("Value converted to base unit meter: " + str(norm_value))
		return norm_value
	
	def convertToDollar(self, orig_value, orig_unit):
		orig_value_parsed = float(orig_value)
		norm_value = None
		if orig_unit == MonetaryUnits.EURO.value:
			norm_value = 1.0851*orig_value
		elif orig_unit == MonetaryUnits.DOLLAR.value:
			norm_value = orig_value
		else:
			sys.exit('ERROR: Conversion to meter failed.')

		print("Value converted to base unit US dollar: " + str(norm_value))
		return norm_value
