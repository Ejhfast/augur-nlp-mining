import urllib2

request = urllib2.Request("http://www.enchantedlearning.com/wordlist/householddevices.shtml")
response = urllib2.urlopen(request)
the_page = response.read()
print the_page