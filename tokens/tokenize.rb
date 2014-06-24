# USE: ruby tokenize.rb corpus-clean.tsv > all-tokens.tsv
# Creates a list of tokens, along with their counts
# Only keeps tokens where the subject is a person
# E.g., the person  walks  the dog  555

require 'pp'

hash = Hash.new(0)
ARGF.each_line do |line|
  line = line.force_encoding('UTF-8')
  tokens = line.split("\t")
  action = tokens.drop(2)
  if ["he","she","you","i","we","they"].include?(action[0])
    hash[action.drop(1)] += 1
  end
end

hash.sort_by { |k,v| v*-1 }.each do |x|
  puts "the person\t#{x[0].join("\t").strip}\t#{x[1]}"
end