class Range:
	# Here, the range around the query value in which results can
	# fall is specified.
	def getRange(self, query_value):
		# TODO insert intelligence that depends on size of input
		try:
			return 0.1*query_value	
		except Exception:
			raise RuntimeError("Range calculation failed!")