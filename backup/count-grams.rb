counts = Hash.new(0)

ARGF.each_line do |line|
  tokens = line.split("\t")
  counts[tokens] += 1
end

#todo dynamic output instead of static output
#todo some kind of string similarity measure instead of having them be exactly the same
counts.sort_by{|k,v| v*-1 }.each do |el|
  if el[1] >= 1
    puts "#{el[0].join("\t").strip}\t#{el[1]}"
  end
end