# USE: ruby strip.rb corpus-clean.tsv | ruby collapse-nop.rb - | ruby skip-gram.rb | -
# Preparse data for the bigram model (each "gram" being a S-V-O action)
# Allows skipgrams up to SKIP

SKIP = 10

require 'pp'
ARGF.each_line.each_cons(3) do |group|
  if !(group.first =~ /NOP/)
    # we want THING -> NOP X -> THING
    a1, a2 = [group.first, group.last].map do |x|
      x.split("\t").drop(2).join(" ").strip
    end
    space = group[1].split(" ").last.to_i
    puts "#{a1}\t#{a2}\t#{space}" if space < SKIP
  end
end
