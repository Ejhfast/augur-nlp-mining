import fileinput
import csv

for line in fileinput.input():
	line = line.decode("ascii", "ignore")
	row = line.split('\t')
	print '\t'.join(row[-3:]).rstrip()
