import sys

def words(s):
	c = len(s.split())

	return c

def chars(s):
	c = len(s)

	return c

if __name__ == "__main__":

	with open(sys.argv[2], 'r') as fd:
		s = fd.read()

	if (sys.argv[1] == '-w'):
		print(words(s))
	elif (sys.argv[1] == '-c'):
		print(chars(s))
	else:
		raise Exception('Invalid argument.')




