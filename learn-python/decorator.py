from time import time

def timer(func):
	def f(*args, **kwargs):
		before = time()
		rv = func(*args, **kwargs)
		after = time()

		print('Elapsed: ', after - before)
	
		return rv

	return f

@timer
def add3(x, y, z):
	return x + y + z

@timer
def sub(x, y):
	return x - y


print('add3: ', add3(3, 5, 6))
print('sub: ', sub(8, 2))

