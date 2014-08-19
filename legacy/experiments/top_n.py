import sys

f1 = sys.argv[1]
f2 = sys.argv[2]
n = int(sys.argv[3])

GRAM_L = 1

def extract_grams(file):
  count = 0
  grams = set([])
  with open(file) as f:
    for line in f:
      if count > n:
        break
      count += 1
      items = line.split("\t")
      gram = items[0:GRAM_L]
      grams.add(" ".join(gram))
  return grams

f1_grams = extract_grams(f1)
f2_grams = extract_grams(f2)

print("{} - {}".format(f1,f2))
print(f1_grams.difference(f2_grams))
print("{} - {}".format(f2,f1))
print(f2_grams.difference(f1_grams))
