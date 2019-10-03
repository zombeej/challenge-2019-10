#!/usr/bin/env ruby
#

require 'time'
require 'json'

t = Time.now.to_f * 1000

# Load data files.
words = File.read('../data/dictionary.txt').split("\n")
letters = JSON.parse(File.read('../data/letters.json'))

re = Regexp.new("^[#{ARGV[0]}]+$")
occ = ARGV[0].each_char.reduce({}) do |h, c|
  h[c] ||= 0
  h[c] += 1
  h
end

validlist = words.
  select { |word| re.match(word) }.
  select do |word|
    # Select only possible words, by letter occurences.
    word.each_char.reduce({}) do |h, c|
      h[c] ||= 0
      h[c] += 1
      h
    end.reduce(true) do |b, c|
      b && occ[c[0]] >= c[1] 
    end
  end.
  map do |w|
    score = w.each_char.reduce(0) { |s, c| s + letters[c]['score'] }
    [ w, score ]
  end.
  max { |j,k| j[1] - k[1] }

t = (Time.now.to_f * 1000 - t)

word = validlist[0]
score = validlist[1] 

puts "basking2, ruby, #{word}, #{score}, #{t}, ARG: #{ARGV}"

