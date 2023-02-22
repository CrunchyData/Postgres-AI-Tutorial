require './db'
require 'nokogiri'

#recipes_xml = Nokogiri::XML(File.read('ArmedForcesRecipes-truncated.xml'))
recipes_xml = Nokogiri::XML(File.read('ArmedForcesRecipes.xml'))

for recipe_xml in recipes_xml.xpath('/*/recipe')
  recipe_id = DB[:recipes].insert(
    name: recipe_xml["description"],
    description: recipe_xml.xpath(".//XML_MEMO1")[0]&.text
  )

  for ingredient_xml in recipe_xml.xpath(".//RecipeItem")
    ingredient_id = nil
    ingredient = DB[:ingredients].where(name: ingredient_xml["ItemName"]).first

    if ingredient.nil?
      ingredient_id = DB[:ingredients].insert(
        name: ingredient_xml["ItemName"]
      )
    else
      ingredient_id = ingredient["id"]
    end

    DB[:recipe_ingredients].insert(
      recipe_id: recipe_id,
      ingredient_id: ingredient_id,
      quantity: ingredient_xml["itemQuantity"],
      unit_key: ingredient_xml["itemMeasureKey"]
    )
  end
end