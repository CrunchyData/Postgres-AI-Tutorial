# Postgres + AI Tutorial

This code and data package accompanies a blog post written by the Crunchy Data team.  Check it out at blog.crunchydata.com

## Contents

The data packet contains the following:

- ArmedForcesRecipes.xml - list of recipes
- parser.rb - a file for parsing the XML and loading it into a Postgres database
- classfier.rb - a file for that returns the OpenAI embeddings for the recipes
- recipe-tracker.sql - a SQL dump from a database ready to query

## Speedrun Walk Through

1. Load the data into a Postgres database:

```bash
bash> cat recipe-tracker.sql | psql recipe_tracker
```

2. Run the following query against your database:

```sql
SELECT
        recipe_1.id,
        recipe_1.name,
        recipe_2.id,
        recipe_2.name
FROM (SELECT * FROM recipes WHERE name = 'Dish, turkey, curry') recipe_1,
        recipes AS recipe_2
WHERE recipe_1.id != recipe_2.id
ORDER BY recipe_1.embedding <=> recipe_2.embedding
LIMIT 10;
```

You’ll get the recommendations for the following similar meals:

```
 id  |        name         | id  |                  name
-----+---------------------+-----+----------------------------------------
 272 | Dish, turkey, curry | 271 | Dish, turkey & noodles, baked
 272 | Dish, turkey, curry | 251 | Dish, pot pie, turkey
 272 | Dish, turkey, curry | 675 | Soup, tomato
 272 | Dish, turkey, curry | 659 | Soup, chicken rice
 272 | Dish, turkey, curry | 672 | Soup, rice w/beef
 272 | Dish, turkey, curry | 660 | Soup, chicken vegetable/Mulligatawny
 272 | Dish, turkey, curry | 199 | Dish, chicken, a la king
 272 | Dish, turkey, curry |  38 | Beef, simmered
 272 | Dish, turkey, curry | 689 | Stuffing, savory bread
 272 | Dish, turkey, curry | 686 | Stew, beef chunks, w/juices & veg, cnd
(10 rows)
```

## Typical Walk Through

1. Install the necessary Ruby gems: `bundle install`
2. Create a Postgres database, and run `create extension vector;`.  If you need a Postgres database, checkout [Crunchy Bridge](https://crunchybridge.com/).
3. Sign up for OpenAI, and get your API token
4. Set `DATABASE_URL` to the Postgres connection string, and set `OPENAI_API_KEY` to the value from #3
4. Parse the `ArmedForcesRecipes.xml` file and load it into the database by running `ruby parser.rb`
7. Pull down the OpenAI embeddings for your recipes by running `ruby classfier.rb` (will take ~ 5 minutes due to rate limiting)
8. Query the database to find similar recipes:

```sql
SELECT
        recipe_1.id,
        recipe_1.name,
        recipe_2.id,
        recipe_2.name
FROM (SELECT * FROM recipes WHERE name = 'Dish, turkey, curry') recipe_1,
        recipes AS recipe_2
WHERE recipe_1.id != recipe_2.id
ORDER BY recipe_1.embedding <=> recipe_2.embedding
LIMIT 10;
```

That is it. Now you have an AI powered recommendation engine.
