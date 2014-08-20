from collections import defaultdict
import pprint
import fileinput

a = defaultdict(dict)
for line in fileinput.input():
	token  = line.rstrip().split('\t')
	if len(token) != 3:
		continue
	[first, second, freq] = token
	freq = int(freq)
	if second in a[first]: freq += a[first][second]
	a[first].update({second: freq})

items = ((k, k2, v) for k in a for k2, v in a[k].items())
ordered = sorted(items, key=lambda x: x[-1], reverse=True)
pprint.pprint(ordered[:200])
