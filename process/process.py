from __future__ import print_function
from nltk.corpus import names
from collections import defaultdict
import operator
import fileinput
import itertools
import sys
import re
import argparse
import csv
import multiprocessing as mp
import subprocess


DEFAULT_INPUT = '../files/watpad.tsv'
DEFAULT_WHITELIST = '../files/sampwhitelist.txt'

def check_whitelist(actions):
	return len(whitelist.intersection(" ".join(actions).split())) > 0

# Utils
def each_cons(xs, n):
	return itertools.izip(*(itertools.islice(g, i, None) for i, g in enumerate(itertools.tee(xs, n))))
def interleave(item,ls): return sum(([item,i] for i in ls), ls[0:1])
def n_filters(filters,stream):
	for f in filters: stream = itertools.ifilter(f,stream)
	for i in stream: yield i
def out_error(string, clear=True): 
	if clear:
		sys.stderr.write("\x1b[2J\x1b[H")
	print(string, file=sys.stderr)
def gram_list(counts,n):
	top = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
	return "\n".join([k+"\t"+str(v) for k,v in itertools.islice(top,0,n)])

# Replace names
def pre_filter(iter):
	nameswords = set([word.lower() for word in names.words()])
	def replace(s): return ' '.join(['he' if x in nameswords else x for x in s.split()])
	for i, line in enumerate(iter):
		if(i%100000==0): out_error("Processed " + str(i) + " lines.", False)
		yield [replace(c) for c in line]

# Filter for persons and objects
def person_filter(iter):
	count = 0
	subjects = set(["i", "you", "he", "she", "we", "they"])
	objects = set(["me", "you", "him", "his", "her", "us", "them", "#", "i", "you", "he", "she", "we", "they", "it"])
	def subject_match(actions):
		return True if len(subjects.intersection(actions[0].split())) > 0 else False
	def object_match(actions):
		if(len(actions) < 3): return False # no object?
		return True if len(objects.intersection(actions[2].split())) == 0 else False
	def approve(actions):
		return all([subject_match(actions), object_match(actions)])
	for group in each_cons(iter, 2):
		count += 1
		if(all([approve(a) for a in group]) & any([check_whitelist(a) for a in group])):
			count = 0
			wrap = [dict(kind="ACTION",value=" ".join(a[1:])) for x in group]
			with_nops = [dict(kind="NOP",value=count)] + interleave(dict(kind="NOP",value=0), wrap)
			for wrapped_item in with_nops: yield wrapped_item

def skip_grams(iter):
	n, skip = 2, 10
	def action_first(seq): return seq[0]["kind"] == "ACTION" # We want: A -> NOP -> A ...
	def skip_check(seq): return reduce(operator.and_, [x["value"] < skip for x in seq if x["kind"] == "NOP"])
	for grp in n_filters([action_first,skip_check], each_cons(iter, 2*(n-1)+1)):
		just_strings = [x["value"] for x in grp if x["kind"] == "ACTION"]
		if len(set(just_strings)) > 1: yield just_strings

def count_grams(iter):
	counts = defaultdict(int)
	for n_gram in iter:
		counts["\t".join(n_gram)] += 1
		yield counts

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('input', nargs='?', default =DEFAULT_INPUT)
	parser.add_argument('wl', nargs='?', type=argparse.FileType('r'), default=open(DEFAULT_WHITELIST))
	return parser.parse_args()

def processChunk(filename, start, end):
	mylines = itertools.islice(open(filename), start, end)
	ticker, last_grams = 0, None
	reader = csv.reader(mylines, delimiter ='\t')
	pipeline = count_grams(skip_grams(person_filter(pre_filter(reader))))
	for ngram_counts in pipeline:
		ticker += 1
		last_grams = ngram_counts
		if(ticker%1000==0):
			display = gram_list(ngram_counts,20)
			out_error(display)
	final_output = gram_list(last_grams,None)
	print(final_output)

def processAll(filename):
	pool = mp.Pool(mp.cpu_count())
	num_segments = mp.cpu_count()
	total_size = int(subprocess.check_output('wc -l ' + filename, shell=True).rstrip().split()[0])
	segment_size = int(total_size/num_segments);
	print(segment_size, num_segments)
	total = []
	for i in xrange(num_segments):
		pool.apply_async(processChunk, [filename, segment_size*i, segment_size*(i+1)])
	pool.close()
	pool.join()

if __name__ == "__main__":
	csv.field_size_limit(sys.maxsize)
	args = parse()
	whitelist = set(args.wl.read().split())
	processAll(args.input)
