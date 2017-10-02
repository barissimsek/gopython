import random

'''
Random file mixer

This small piece of code mixes lines randomly from a given file.
It's important to have random dataset to train your machine learning algorithm.
But mostly the data comes from structured sources so that it is may not be random.

It reads data from a file named dataset.csv and prints on stdout.
If needed redirect stdout to a file to have the random data as a file.

# python mixer.py > mixed.csv

-simsek
'''

with open('dataset.csv','r') as source:
	data = [ (random.random(), line) for line in source ]

data.sort()

for _, line in data:
	print line.strip()

