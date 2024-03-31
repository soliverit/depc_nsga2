##
# Printing to console sucks. Make life easier by adding helper functions here
##
class PrintHelper():
	##
	# Pad a string with the padChar to the target length
	#
	# Output: string padded. E.g input="Fire", length=6, padChar="-" outputs "Fire--"
	##
	@staticmethod
	def Pad(input, length, padChar=" "):
		input	= str(input)
		while len(input) < length:
			input += padChar
		return input
	##
	# Pad method but for arrays
	#
	# Output: string concatenated padded values
	##
	def PadArray(array, length, padChar=" "):
		return "".join([ __class__.Pad(val, length, padChar) for val in array])