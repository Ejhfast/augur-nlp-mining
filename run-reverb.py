#generates the corpus-clean output

import subprocess
import StringIO
import csv
import sys

filepath = sys.argv[1]
numfiles = sys.argv[2]

scsv = subprocess.check_output("find " + filepath + " |  grep -e '[4-7][0-9]' | head -" + numfiles + " | java -Xmx512m -jar reverb.jar -f", shell=True) 
f = StringIO.StringIO(scsv)
reader = csv.reader(f, delimiter='\t')
for row in reader:
	print '\t'.join(row[:5])

