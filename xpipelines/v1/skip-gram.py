import itertools
import fileinput
import re

# thank you stackoverflow...
def each_cons(xs, n):
  return itertools.izip(*(itertools.islice(g, i, None) for i, g in enumerate(itertools.tee(xs, n))))

n = 2
skip = 10

for grp in each_cons(fileinput.input(), 2*(n-1)+1):
  if not re.search("NOP", grp[0]):
    parsed = [int(i.split(" ")[-1]) if re.search("NOP",i) else i for i in grp]
    if reduce(lambda x, y: x & y, [x < skip for x in parsed if isinstance(x,int)]):
      strings = [" ".join(x.split("\t")).rstrip() for x in parsed if isinstance(x,str)]
      if len(set(strings)) > 1: print "\t".join(strings)
