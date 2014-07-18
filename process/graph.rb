# Create data that generates a force-directed graph
# Only currently usable on subsets of the data, (e.g., grep "dinner" bigrams.tsv)

require 'json'

def blacklist(grp)
  no = ["looked","said"]
  no.each do |bad|
    if(grp[0] == bad || grp[1] == bad)
      return true
    end
  end
  return false
end

count_hash = Hash.new { |h,k| h[k] = [] }
raw = IO.read(ARGV[0]).split("\n").map { |x| x.split("\t").map { |x| x.strip } }
raw.each do |grp|
  count_hash[grp[0]].push([grp[1],grp[2].to_i]) if grp[2].to_i > 5 && (!blacklist(grp))
end
bigrams = []
count_hash.default = nil
d = Marshal.load(Marshal.dump(count_hash))
count_hash.each do |k,v|
  best = v.sort_by{ |x| (x[1] * -1).to_f / (d[x[0]] ? d[x[0]].size : 1)  }.take(1).map { |x| x[0] }
  best.each do |k2|
    bigrams.push([k,k2])
  end
end

#bigrams = IO.read(ARGV[0]).split("\n").select{ |x| x.split("\t").last.to_i > 50 && x.split("\t").last.to_i < 200  }.map { |x| x.split("\t").take(2).map{ |x| x.gsub("the person","") } }

mapping = Hash.new { |h,k| h[k] = [] }
bigrams.each { |gram| mapping[gram[0]].push(gram[1]) }

uniq_grams = bigrams.reduce(:+).uniq

nodes = []
edges = []
index_track = {}

uniq_grams.each do |k|
  index_track[k] = nodes.size
  nodes.push({ 'name' => k })
end
mapping.keys.each do |src|
  mapping[src].each do |tgt|
    edges.push({"source" => index_track[src], "target" => index_track[tgt], "value" => 1 })
  end
end

puts ({'nodes' => nodes, 'links' => edges }).to_json
