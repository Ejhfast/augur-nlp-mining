import sys


print len(sys.argv)

data = None
if(len(sys.argv) >= 2):
	data = sys.argv[1].readlines()
else:
	data = sys.stdin.readlines()

SKIP = 10

def group(seq, n):
	return (seq[i:i+n] for i in range(len(seq)-n+1))

g = filter(lambda x: True if "NOP" in x[1] else False, list(group(data,3))) 
print g