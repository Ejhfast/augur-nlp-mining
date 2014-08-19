from relgrams import *
import csv

if __name__ == '__main__':
	with open('../files/re-bi-custom.tsv', 'rb') as csvfile:
		csvfile = csv.reader(csvfile, delimiter='\t')
		outputs = reverb_like_thing("he rode the bike.");
		print outputs
		for line in csvfile:
			for output in outputs:
				if line[0].split(' ')[0] == output[0] and line[0].split(' ')[1] == output[1]:
					print line

