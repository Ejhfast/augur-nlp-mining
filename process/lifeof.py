import csv
soFar = []
for line in csv.reader(open("sampout.txt", "r"), delimiter= '\t'):
	#print line[-3:], line[2:5], line[11]
	if(float(line[11])> 0.4):
		if(line[2].lower() == s for s in ["he", "Crick", "Francis"]):
			line[2] = "he	"
			soFar.append(' '.join(line[2:5]))


#print soFar
print ('. ').join(soFar)