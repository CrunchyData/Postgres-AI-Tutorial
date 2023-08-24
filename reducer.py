import os
import psycopg2
import ast

# Connect to your SQLite database
conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
cursor = conn.cursor()

# Initialize vector_summation list
vector_summation = []

cursor.execute("SELECT id, embedding FROM recipes WHERE embedding IS NOT NULL")

# Fetch data from the recipes table
for row in cursor:
    recipe_id, embedding = row[0], row[1]

    # Evaluate the embedding string into a list of vectors
    vectors = ast.literal_eval(embedding)

    # Iterate through vectors and update vector_summation
    for index, vector in enumerate(vectors):
        if len(vector_summation) <= index:
            vector_summation.append({'index': index})

        vector_summation[index]['max'] = max(vector_summation[index].get('max', vector), vector)
        vector_summation[index]['min'] = min(vector_summation[index].get('min', vector), vector)

# Sort vector_summation by max - min difference and select the last 50 and 10 elements
vector_summation.sort(key=lambda x: x['max'] - x['min'])
vector_index = [v['index'] for v in vector_summation[-50:]]
super_compressed = [v['index'] for v in vector_summation[-10:]]

# Update recipes with compacted_embedding and super_compacted_embedding
cursor.execute("SELECT id, embedding FROM recipes WHERE compacted_embedding IS NULL AND embedding IS NOT NULL")

# Open an update cursor so we can update while keeping the select cursor open
update_cursor = conn.cursor()

for row in cursor:
    recipe_id, embedding = row[0], row[1]
    vectors = ast.literal_eval(embedding)

    compacted_vector = [vectors[index] for index in vector_index]
    super_compressed_vector = [vectors[index] for index in super_compressed]

    # Update the database with the compacted and super compressed embeddings
    update_cursor.execute("UPDATE recipes SET compacted_embedding = %s, super_compacted_embedding = %s WHERE id = %s", (str(compacted_vector), str(super_compressed_vector), recipe_id))

# Close the database connection
conn.commit()
conn.close()
