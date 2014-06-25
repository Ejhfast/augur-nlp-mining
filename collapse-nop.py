#todo: combine with filter-actions
import fileinput

count_nop = 0

for line in fileinput.input():
  if line.strip() == "NOP":
    count_nop += 1
  else:
    print "NOP ", count_nop
    print line.rstrip()
    count_nop = 0