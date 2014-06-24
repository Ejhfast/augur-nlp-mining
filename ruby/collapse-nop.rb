# USE: ruby filter-actions.rb corpus-clean.tsv | ruby collapse-nop.rb -
# Collapse adjacent NOPs

count_nop = 0
ARGF.each_line do |line|
  if line.strip == "NOP"
    count_nop += 1
  else
    puts "NOP #{count_nop}"
    puts line
    count_nop = 0
  end
end
