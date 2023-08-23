#!/Users/christopherwinslett/.rbenv/shims/ruby

require 'bundler'
Bundler.require
Dotenv.load

require './db'

vector_summation = []

DB[:recipes].each do |recipe|
  next if recipe[:embedding].nil?
  vectors = eval(recipe[:embedding])

  vectors.each_with_index do |vector, index|
    vector_summation[index] ||= {index: index}
    vector_summation[index][:max] = [vector_summation[index][:max], vector.to_f].compact.max
    vector_summation[index][:min] = [vector_summation[index][:min], vector.to_f].compact.min
  end
end

vector_index = vector_summation.sort_by { |vector| vector[:max] - vector[:min] }[-50..-1].map { |v| v[:index] }
super_compressed = vector_summation.sort_by { |vector| vector[:max] - vector[:min] }[-10..-1].map { |v| v[:index] }

while recipe = DB[:recipes].where(compacted_embedding: nil).exclude(embedding: nil).first do
  next if recipe[:embedding].nil?
  vectors = eval(recipe[:embedding])

  compacted_vector = vector_index.inject([]) { |new_embedding, index| new_embedding << vectors[index] }.inspect
  super_compressed_vector = super_compressed.inject([]) { |new_embedding, index| new_embedding << vectors[index] }.inspect

  DB[:recipes].where(id: recipe[:id]).update(compacted_embedding: compacted_vector, super_compacted_embedding: super_compressed_vector)
end
