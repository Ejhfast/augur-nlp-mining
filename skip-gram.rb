# Preparse data for the n-gram model (each "gram" being a S-V-O action)
# Allows skipgrams up to SKIP

require 'logger'

logger = Logger.new('log.txt')

SKIP = 10
LEN = 2 # n for n-gram

magic = 2*(LEN-1)+1

#todo remove where the second action is the same as the first one
ARGF.each_line.each_cons(magic) do |group|
  if !(group.first =~ /NOP/)
    parsed = group.map { |x| x =~ /NOP/ ? x.split(" ").last.to_i : x }
    if parsed.select { |x| x.is_a? Integer }.map { |x| x < SKIP }.reduce(:&)
      strings = parsed.select { |x| x.is_a? String }.map do |x|
        x.split("\t").join(" ").strip
    	end
      puts strings.join("\t")
    end
  end
end
