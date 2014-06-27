from bs4 import BeautifulSoup
import urllib2


#request = urllib2.Request("")
#response = urllib2.urlopen(request)


html_doc = open('sample.html','r')
soup = BeautifulSoup(html_doc)
tables = soup.find_all('table')
print filter(lambda x: len(x) > 1, tables[2].text.split())

print map(unicode,tables[3].find_all('a'))