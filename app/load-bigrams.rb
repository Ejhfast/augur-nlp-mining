require 'mongoid'
require 'pp'

Mongoid.load!('mongoid.yml',:development)

class Bigram
  include Mongoid::Document
  field :v1, type: String
  field :o1, type: String
  field :v2, type: String
  field :o2, type: String
  filed :count, type: Integer
end

ARGF.each_line do |line|
  parts = line.split("\t")
  v1 = parts[0]
  o1 = parts[1]
  v2 = parts[3]
  o2 = parts[4]
  count = parts[6].to_i
  Bigram.new({v1: v1, o1: o1, v2: v2, o2: o2, count: count}).save!
  #pp({v1: v1, o1: o1, v2: v2, o2: o2, count: count})
end
