'''

Simsek's K-Neighborhood Distance

To get better results from MIMIC_MAP use case sensitive strings. 

'''

K_CONFIDENCE = 2
DELIMITERS = ['.', '-', '_']
MIMIC_MAP = {
	'a': '@',
	'i': '!',
	'o': '0',
	'B': '3',
	'1': 'I'
}

def skdistance(str1, str2, k):
	# Normalize mimics
	for key, val in MIMIC_MAP.iteritems():
		str1 = str1.replace(val, key)
		str2 = str2.replace(val, key)

	# Normalize delimiters
	for d in DELIMITERS:
		str1 = str1.replace(d, '')
		str2 = str2.replace(d, '')

	# similarity around k-neighborhood
	s = 0
	for i in range(len(str1)):
		for j in range(k):
			if i + j < len(str2):
				rindex = i + j
				if str1[i] == str2[rindex]:
					s += 1
					break

			if len(str2) > i - j > 0:
				lindex = i - j
				if str1[i] == str2[lindex]:
					s += 1
					break

	d = len(str1) - s

	return d

if __name__ == "__main__":
	
	d = skdistance("bankofamerica", "bankamoferica", 3)

	print "Distance: " + str(d)


