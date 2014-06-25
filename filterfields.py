import fileinput
import csv

for line in fileinput.input():
	row = line.split('\t')
	print '\t'.join(row[-3:])