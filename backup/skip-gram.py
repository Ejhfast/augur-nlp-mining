import sys

def group(seq, n):
	return (seq[i:i+n] for i in range(len(seq)-n+1))

data = None
if(len(sys.argv) >= 2):
	data = sys.argv[1].readlines()
else:
	data = sys.stdin.readlines()

SKIP = 10

def customprint(x):
	[a,b] = [' '.join(y.split('\t')[2:]).rstrip() for y in [x[0], x[2]]]
	print a + '\t' + b + '\t' + x[1].split(' ')[-1].rstrip()

g = filter(lambda x: True if "NOP" in x[1] and int(x[1].split(' ')[-1]) < SKIP else False, list(group(data,3)))
map(customprint , g)