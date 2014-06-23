# USE: ruby count-grams.rb bigrams-file.tsv\
# Creates the bigram model

counts = Hash.new(0)

ARGF.each_line do |line|
  tokens = line.split("\t")
  actions = tokens.reverse.drop(1).reverse
  counts[actions] += 1
end

counts.sort_by{|k,v| v*-1 }.each do |el|
  if el[1] > 1
    puts "#{el[0].join("\t").strip}\t#{el[1]}"
  end
end
