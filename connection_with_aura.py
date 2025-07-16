import json
from neo4j import GraphDatabase

URI = "neo4j+s://d498e8b5.databases.neo4j.io"
AUTH = ("neo4j", "Fpt-HFQcO89FrCR-fTDN1z3Lbvu6wJfDkb2Wqsc-m68") 

# Path to your local JSON file
LOCAL_JSON_FILE = "/Users/ridaiftikhar/Library/Application Support/neo4j-desktop/Application/Data/dbmss/dbms-a2cf2a66-f9a4-4ac5-ae50-e917d98373ff/import/result_2021.json" 

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity() # Checks connection

    print("Connection to Aura established. Loading data...")

    with open(LOCAL_JSON_FILE, 'r') as f:
        articles_data = json.load(f)

    with driver.session() as session:
        # Cypher query to import article
        query = """
        UNWIND $articles AS article
        MERGE (a:Article {url: article.url})
        SET a.title = article.title,
            a.date = article.date

        MERGE (s:Source {name: article.source})
        MERGE (a)-[:PUBLISHED_BY]->(s)

        WITH a, article, apoc.text.split(article.author, " and ") AS authorList

        UNWIND authorList AS authorName
        WITH a, trim(authorName) AS authorName, article
        WHERE authorName <> ""
        MERGE (auth:Author {name: authorName})
        MERGE (a)-[:WRITTEN_BY]->(auth)

        WITH a, article.keywords AS keywordsList
        UNWIND keywordsList AS keywordName
        MERGE (k:Keyword {name: keywordName})
        MERGE (a)-[:HAS_KEYWORD]->(k)
        """

        # Split data into batches 
        batch_size = 2000 
        for i in range(0, len(articles_data), batch_size):
            batch = articles_data[i : i + batch_size]
            try:
                session.run(query, articles=batch)
                print(f"Processed batch {i // batch_size + 1} of {len(articles_data) // batch_size + 1}")
            except Exception as e:
                print(f"Error processing batch starting at index {i}: {e}")
                break 

    print("Data upload complete ")
