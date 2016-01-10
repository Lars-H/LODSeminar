# Here, the range around the query value in which results can fall is specified.
def getRange(query_value, logString='RANGE - '):
	# TODO insert intelligence that depends on size of input
	#try:
	range = 0.1*query_value
	print(logString + "Range is " + str(range) + ", meaning values between " + \
			str(query_value-range/2) + " and " + \
			str(query_value+range/2) + " can be returned.")
	return range	
	#except Exception:
	#	raise RuntimeError("Range calculation failed!")