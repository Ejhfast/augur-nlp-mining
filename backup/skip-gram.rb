# Preparse data for the n-gram model (each "gram" being a S-V-O action)
# Allows skipgrams up to SKIP

SKIP = 10
LEN = 2 # n for n-gram

magic = 2*(LEN-1)+1

ARGF.each_line.each_cons(magic) do |group|
  if !(group.first =~ /NOP/)
    parsed = group.map { |x| x =~ /NOP/ ? x.split(" ").last.to_i : x }
    if parsed.select { |x| x.is_a? Integer }.map { |x| x < SKIP }.reduce(:&)
      strings = parsed.select { |x| x.is_a? String }.map do |x|
        x.split("\t").join(" ").strip
    	end
      puts strings.join("\t") if strings.uniq.size > 1
    end
  end
end
