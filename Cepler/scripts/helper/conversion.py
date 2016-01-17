from properties import Mapping
from units import MassUnits, DistanceUnits, MonetaryUnits
import eurusd
import requests
import os


def convert(orig_value, orig_unit, quantity, logString):
	norm_value = None
	if (quantity == Mapping.WEIGHT):
		norm_value = convertToKilogram(orig_value, orig_unit, logString)
	elif (quantity == Mapping.DISTANCE):
		norm_value = convertToMeter(orig_value, orig_unit, logString)
	elif (quantity == Mapping.COST):
		norm_value = convertToDollar(orig_value, orig_unit, logString)
	else:
		raise RuntimeError('Conversion failed because quantity was not properly set.')

	return norm_value

def convertToKilogram(orig_value, orig_unit, logString):
	orig_value_parsed = float(orig_value)
	norm_value = None
	if orig_unit == MassUnits.TON.value:
		norm_value = 1000*orig_value
	elif orig_unit == MassUnits.KILOGRAM.value:
		norm_value = orig_value
	elif orig_unit == MassUnits.GRAM.value:
		norm_value = orig_value/1000
	else:
		raise RuntimeError('Conversion to kilogram failed.')

	print(logString + "Value converted to base unit kilogram: " + str(norm_value))
	return norm_value

def convertToMeter(orig_value, orig_unit, logString):
	orig_value_parsed = float(orig_value)
	norm_value = None
	if orig_unit == DistanceUnits.KILOMETER.value:
		norm_value = 1000*orig_value
	elif orig_unit == DistanceUnits.METER.value:
		norm_value = orig_value
	elif orig_unit == DistanceUnits.CENTIMETER.value:
		norm_value = orig_value/100
	else:
		raise RuntimeError('Conversion to meter failed.')

	print(logString + "Value converted to base unit meter: " + str(norm_value))
	return norm_value

def convertToDollar(orig_value, orig_unit, logString):
	orig_value_parsed = float(orig_value)
	norm_value = None
	if orig_unit == MonetaryUnits.EURO.value:
		norm_value = curlCurrencyConversion(logString)*orig_value
	elif orig_unit == MonetaryUnits.DOLLAR.value:
		norm_value = orig_value
	else:
		raise RuntimeError('Conversion to meter failed.')

	print(logString + "Value converted to base unit US dollar: " + str(norm_value))
	return norm_value

# Convert Euro to Dollar
def curlCurrencyConversion(logString):
	
	# try to communicate with Yahoo Finance API
	try:
		r = requests.get('http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=EURUSD=X')
		print(logString + 'Yahoo Finance API result: ' + r.text),
		print(os.getcwd())
		f = open(os.getcwd() + '/helper/eurusd.py','w')
		f.write("rate = " + r.text.split(',').pop(1))
		f.close()
		reload(eurusd)
	except requests.exceptions.ConnectionError:
		r = None
		print(logString + 'Yahoo Finance API call not successful, taking lately queried conversion rate.')
	
	# read from file, no matter if API call was successful
	return eurusd.rate