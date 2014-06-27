# Create data that generates a force-directed graph
# Only currently usable on subsets of the data, (e.g., grep "dinner" bigrams.tsv)

require 'json'

bigrams = IO.read(ARGV[0]).split("\n").map { |x| x.split("\t").take(2).map{ |x| x.gsub("the person","") } }

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
