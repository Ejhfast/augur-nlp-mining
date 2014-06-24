#generates the corpus-clean output

import subprocess
import StringIO
import csv
import sys

numfiles = None

if (len(sys.argv) < 2):
	raise NameError('Usage: python ' + sys.argv[0] + '.py filepath [numfiles]')
if (len(sys.argv) > 2):
	numfiles = sys.argv[2]

filepath = sys.argv[1]
command = None
if(numfiles == None):
	command = "find " + filepath + " |  grep -e '[4-7][0-9]' | java -Xmx512m -jar reverb.jar -f | tee watpad.tsv"
else:
	command = "find " + filepath + " |  grep -e '[4-7][0-9]' | head -" + numfiles + " | java -Xmx512m -jar reverb.jar -f | tee watpad.tsv"

scsv = subprocess.check_output(command, shell=True)
f = StringIO.StringIO(scsv)
reader = csv.reader(f, delimiter='\t')
for row in reader:
	print '\t'.join(row[:5])
