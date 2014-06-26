# USE: ruby filter-tokens.rb all-tokens.tsv
# Throws away tokens thatinclude actions on other people, and tokens that don't occur frequently enough

MIN = 100

def replace(word)
  if ["he", "she", "him", "i", "myself", "you", "me", "himself", "herself", "yourself"].include?(word)
    "the person"
  elsif ["they", "them", "we", "us", "ourselves", "themselves"].include?(word)
    "the people"
  else
    word
  end
end

object_match = ["the person", "the people", "it", "her",
                "that", "this", "#", "there", "all", "'s", "the #"]

ARGF.each_line do |line|
  replace_pronouns = line.split("\t").map do |seg|
    seg.split(" ").map { |word| replace(word) }.join(" ")
  end
  if !object_match.include?(replace_pronouns[2].strip)
    puts replace_pronouns.join("\t") if replace_pronouns[3].to_i >= MIN
  end
end
