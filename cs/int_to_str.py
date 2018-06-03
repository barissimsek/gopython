#
# Complexity: O(log(n)) 
#

def int_to_str(i):
	digits = '0123456789'
	
	if i == 0: 
		return '0'

	result = ''

	while i > 0:
		result = digits[i%10] + result
		i = i // 10

	return result

if __name__== "__main__":

	print(int_to_str(0))

	print(int_to_str(8))

	print(int_to_str(1807953))

