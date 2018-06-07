from time import sleep

def compute():
	x = 0
	for i in range(10):
		sleep(.5)
		x = x + i
		yield x

for val in compute():
	print(val)
