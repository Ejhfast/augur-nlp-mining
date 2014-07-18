import fileinput
from collections import defaultdict
import operator
import os
import shutil
import random

by_story = defaultdict(set)
by_tag = defaultdict(set)

for line in fileinput.input():
  items = line.split(",")
  for chapter in items[1].split():
    by_story[chapter] = by_story[chapter].union(set(items[4].split()))
  for tag in items[4].split():
    by_tag[tag] = by_tag[tag].union(set(items[1].split()))

tag_counts = { tag:len(s) for tag,s in by_tag.iteritems() }
sorted_tags = sorted(tag_counts.iteritems(), key=operator.itemgetter(1), reverse=True)

def sample(seq,n):
  to_lst = list(seq)
  ids = random.sample(xrange(len(to_lst)),n)
  return [to_lst[i] for i in ids]

genres = ["romance","action"]

for genre in genres:
  chapters = sample(by_tag[genre],2000)
  path = "../files/{}".format(genre)
  os.mkdir(path)
  for chapter in chapters:
    src = "../files/source_text/{}".format(chapter)
    dst = path + "/{}".format(chapter)
    shutil.copyfile(src,dst)
    print("Copying {} to {}".format(src,dst))

# count = 0
# for k,v in by_story.iteritems():
#   count += 1
# print(count)
# for tag,c in sorted_tags:
#   print("{}\t{}".format(tag,c))
