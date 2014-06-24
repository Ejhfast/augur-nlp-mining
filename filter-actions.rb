# USE ruby filter-actions.rb corpus-clean.tsv
# Only keeps tokens from the approved list
# Also removes actions that are oriented towards other people (that have people as objects)
# Replaces filtered tokens with NOPs

require 'pp'

# The list of approved tokens. See workflow.txt
APPROVED_LIST = "tokens/approved-combined.tsv"

# Word replacement. Basically, the same thing we did with normalizing tokens.
def replace(word)
  if ["he", "she", "him", "i", "myself"].include?(word)
    "the person"
  elsif ["they", "them", "we", "us", "ourselves"].include?(word)
    "the people"
  else
    word
  end
end

# Create whitelist token hash
whitelist = {}
IO.read(APPROVED_LIST).split("\n").each do |x|
  whitelist[x.split("\t")[0...-1].join(" ")] = true
end

File.foreach(ARGV[0]) do |line|
  line = line.force_encoding('UTF-8')
  tokens = line.split("\t")
  header = tokens.take(2)
  relations = tokens.drop(2)
  relations = relations.map do |x|
    x.split(" ").map { |y| replace(y.strip) }.join(" ").strip
  end
  if whitelist[relations.join(" ").strip]
    puts [header+relations].join("\t")
  else
    puts "NOP"
  end
end
