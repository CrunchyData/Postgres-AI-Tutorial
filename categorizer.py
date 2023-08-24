import os
import psycopg2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

recipes = []
data = []

# connect to the database
conn = psycopg2.connect(os.environ.get('DATABASE_URL'))

# return the recipes from the database
cursor = conn.cursor()
select_query = "SELECT id, name, category, embedding FROM recipes WHERE embedding IS NOT NULL ORDER BY category NULLS LAST;"
cursor.execute(select_query)

# an array of recipes for lookup later + an array of arrays of embeddings for clustering
# order is important here, so we can match the recipe to the embedding
for row in cursor:
    recipes.append({'id': row[0], 'name': row[1]})
    formatted_entry = [float(x) for x in row[3][1:-1].split(',')]
    data.append(formatted_entry)

# perform k-means clustering
# change 6 to get more or less categories
kmeans = KMeans(n_clusters=6, n_init=100)
kmeans.fit(data)

# group recipes by category
category_lookup = {}
for i in range(len(recipes)):
    if kmeans.labels_[i] in category_lookup:
        category_lookup[kmeans.labels_[i]]['recipe_names'].append(recipes[i]['name'])
        category_lookup[kmeans.labels_[i]]['recipe_ids'].append(recipes[i]['id'])
    else:
        category_lookup[kmeans.labels_[i]] = {'id': kmeans.labels_[i], 'recipe_names': [recipes[i]['name']], 'recipe_ids': [recipes[i]['id']]}

# walk through recipes and ask for category
# then update category based on input
for i in category_lookup:
    print('How would you name the following?')

    for recipe in category_lookup[i]['recipe_names']:
        print('   ' + recipe)

    category = input("category: ")

    update_query = "UPDATE recipes SET category = %s WHERE id = ANY(%s);"
    cursor.execute(update_query, [category, category_lookup[i]['recipe_ids']])
    conn.commit()

conn.close()
