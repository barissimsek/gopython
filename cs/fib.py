'''
Fibonacci numbers

The Fibonacci numbers form a sequence of integers defined recursively
in the following way. The first two numbers in the Fibonacci sequence are 0 and 1,
and each subsequent number is the sum of the previous two.
'''

def fibonacci(N):
	# Initialize the fibonacci series
	# fib(0) = 0, fib(1) = 1
	L = [0] * (N + 1)
	L[1] = 1

	for i in range(2, N+1):
		L[i] = L[i-1] + L[i-2]

	return L[N]

print(fibonacci(10))

