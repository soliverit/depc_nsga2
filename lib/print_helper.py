class PrintHelper():
	@staticmethod
	def pad(input, length, padChar=" "):
		input	= str(input)
		while len(input) < length:
			input += padChar
		return input
	def padArray(array, length, padChar=" "):
		return "".join([ __class__.pad(val, length, padChar) for val in array])