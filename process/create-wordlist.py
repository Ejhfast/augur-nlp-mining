import fileinput
from bs4 import BeautifulSoup
import sys

soup = None
if(len(sys.argv) > 1):
	soup = BeautifulSoup(open(sys.args[1]))
else:
	soup = BeautifulSoup(sys.stdin)
tables = soup.find_all('table')
print ' '.join(filter(lambda x: len(x) > 1, tables[2].text.lower().split()))