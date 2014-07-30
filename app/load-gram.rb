require 'mongoid'
require 'pp'

Mongoid.load!('mongoid.yml',:development)

class Gram
  include Mongoid::Document
  field :verb, type: String
  field :object, type: String
  filed :count, type: Integer
end

ARGF.each_line do |line|
  parts = line.split("\t")
  v = parts[0]
  o = parts[1]
  count = parts[3].to_i
  Gram.new({verb: v, object: o, count: count}).save!
  #pp({v1: v1, o1: o1, v2: v2, o2: o2, count: count})
end
