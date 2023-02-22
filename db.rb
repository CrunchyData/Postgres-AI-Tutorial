require 'sequel'

connection_string = ENV['DATABASE_URL']
DB = Sequel.connect(connection_string)

DB.create_table? :recipes do
  primary_key :id
  String :name
  String :description
  Vector :embedding
end

DB.create_table? :ingredients do
  primary_key :id
  String :name
end

DB.create_table? :recipe_ingredients do
  primary_key :id
  Integer :recipe_id
  Integer :ingredient_id
  String :quantity
  Integer :unit_key
end
