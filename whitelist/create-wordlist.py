import fileinput
from bs4 import BeautifulSoup
import sys

soup = None
if(len(sys.argv) > 1):
	soup = BeautifulSoup(open(sys.argv[1]))
else:
	soup = BeautifulSoup(sys.stdin)

#tables = soup.find_all('table')
#print ' '.join(filter(lambda x: len(x) > 1, tables[3].text.lower().split()))
#print soup.find('p')
#print ' '.join(filter(lambda x: len(x) > 1, tables[3].text.lower().split()))

#if vocabulary.com
print ' '.join(filter(lambda x: True if len(x)>1 and len(x.split())==1 else False, soup.find(id ='wordlist').text.replace('\n\n', '').split('\n')[::2]))