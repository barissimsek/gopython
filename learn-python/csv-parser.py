import csv
import sys

with open(sys.argv[1], 'r') as csvfile:
	addrbook = csv.reader(csvfile, delimiter=',')
	for row in addrbook:
		for col in row:
			print col
		print
