import itertools, os
import multiprocessing as mp
import mmap, subprocess
def slicefile(filename, start, end):
	mylines = itertools.islice(open(filename), start, end)
	return list(mylines)

def wccount(filename):
	out = subprocess.Popen(['wc', '-l', filename],
						 stdout=subprocess.PIPE,
						 stderr=subprocess.STDOUT
						 ).communicate()[0]
	return int(out.partition(b' ')[0])

if __name__ == "__main__":
	pool = mp.Pool(mp.cpu_count())
	num_segments = 20
	total_size = 10477588
	segment_size = int(total_size/num_segments);
	total = []
	print segment_size, num_segments
	for i in xrange(num_segments):
		total.append(pool.apply_async(slicefile, ['../files/watpad.tsv', segment_size*i, segment_size*(i+1)]))
	for i in xrange(20):
		print total[i].get(timeout = 1)