import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

class KnowledgeGraphOperations:
    def __init__(self):
        """
        Initialize KnowledgeGraphOperations with Neo4j connection parameters from .env file.
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize Neo4j connection variables from .env
        self.aura_instancename = os.getenv('AURA_INSTANCENAME')
        self.neo4j_uri = os.getenv('NEO4J_URI')
        self.neo4j_username = os.getenv('NEO4J_USERNAME')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD')
        self.neo4j_database = os.getenv('NEO4J_DATABASE')
        self.auth = os.getenv('AUTH')
        
        # Initialize Neo4j driver
        try:
            self.driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_username, self.neo4j_password)
            )
            print("Neo4j driver initialized successfully")
        except Exception as e:
            print(f"Error initializing Neo4j driver: {e}")
            self.driver = None
        
        print("KnowledgeGraphOperations initialized with environment variables")
    
    def execute_query(self, cypher_query, parameters=None):
        """
        Execute a Cypher query on Neo4j database.
        
        Args:
            cypher_query (str): Cypher query to execute
            parameters (dict): Parameters for the query (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.driver.session(database=self.neo4j_database) as session:
                session.run(cypher_query, parameters)
            return True
        except Exception as e:
            print(f"Error executing query: {e}")
            return False

    def create_source_node(self, source):
        """
        Create a Source node in the knowledge graph.
        
        Args:
            source (dict): Source object with key-value pairs
            
        Returns:
            bool: True if successful, False otherwise
        """
        #print("Creating source node")
        create_source_query = """
        MERGE (s:Source {name: $source_name})
        """
        parameters = {"source_name": source.get("source", "")}
        return self.execute_query(create_source_query, parameters)

    def create_article_node(self, article):
        """
        Create an Article node in the knowledge graph.
        
        Args:
            article (dict): Article object with url, title, author, date, content
            
        Returns:
            bool: True if successful, False otherwise
        """
        #print("Creating article node")
        create_article_query = """
        MERGE (a:Article {url: $url})
        SET a.title = $title,
            a.author = $author,
            a.date = $date,
            a.content = $content
        """
        parameters = {
            "url": article.get("url", ""),
            "title": article.get("title", ""),
            "author": article.get("author", ""),
            "date": article.get("date", ""),
            "content": article.get("content", "")
        }
        return self.execute_query(create_article_query, parameters)

    def create_keyword_node(self, keyword):
        """
        Create a Keyword node in the knowledge graph.
        
        Args:
            keyword (str): Individual keyword string
            
        Returns:
            bool: True if successful, False otherwise
        """
        #print(f"Creating keyword node: {keyword}")
        create_keyword_query = """
        MERGE (k:Keyword {name: $keyword_name})
        """
        parameters = {"keyword_name": keyword}
        return self.execute_query(create_keyword_query, parameters)

    def create_source_article_relationship(self, source_name, article_url):
        """
        Create a PUBLISHED relationship between Source and Article nodes.
        
        Args:
            source_name (str): Name of the source
            article_url (str): URL of the article
            
        Returns:
            bool: True if successful, False otherwise
        """
        #print(f"Creating PUBLISHED relationship: {source_name} -> {article_url}")
        create_relationship_query = """
        MATCH (s:Source {name: $source_name})
        MATCH (a:Article {url: $article_url})
        MERGE (s)-[r:PUBLISHED]->(a)
        """
        parameters = {
            "source_name": source_name,
            "article_url": article_url
        }
        return self.execute_query(create_relationship_query, parameters)

    def create_article_keyword_relationships(self, article_url, keywords_list):
        """
        Create CONSISTS relationships between Article and Keyword nodes.
        
        Args:
            article_url (str): URL of the article
            keywords_list (list): List of keywords for the article
            
        Returns:
            bool: True if successful, False otherwise
        """
        #print(f"Creating CONSISTS relationships for article: {article_url}")
        for keyword in keywords_list:
            if keyword:  # Only create relationships for non-empty keywords
                #print(f"  Creating CONSISTS relationship: {article_url} -> {keyword}")
                create_relationship_query = """
                MATCH (a:Article {url: $article_url})
                MATCH (k:Keyword {name: $keyword_name})
                MERGE (a)-[r:CONSISTS]->(k)
                """
                parameters = {
                    "article_url": article_url,
                    "keyword_name": keyword
                }
                self.execute_query(create_relationship_query, parameters)
        return True

    def insert_data(self, data):
        """
        Insert data into knowledge graph.
        
        Args:
            data: List of news articles to be inserted into the knowledge graph
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not isinstance(data, list):
                print("Error: Data must be a list")
                return False
                
            print(f"Processing {len(data)} articles for knowledge graph insertion...")
            
            for i, article in enumerate(data):
                print(f"\nProcessing article {i+1}:")
                
                # Initialize variables for the three node types
                source_node = {
                    "source": article.get("source", "")
                }
                
                article_node = {
                    "url": article.get("url", ""),
                    "title": article.get("title", ""),
                    "author": article.get("author", ""),
                    "date": article.get("date", ""),
                    "content": article.get("content", "")
                }
                
                keywords_node = {
                    "keywords": article.get("keywords", [])
                }
                
                # Print the initialized node variables
                print(f"  Source Node: {source_node}")
                print(f"  Article Node: {article_node}")
                print(f"  Keywords Node: {keywords_node}")
                
                # Create source node in knowledge graph
                self.create_source_node(source_node)
                
                # Create article node in knowledge graph
                self.create_article_node(article_node)
                
                # Create keyword nodes for each keyword in the array
                keywords_list = keywords_node.get("keywords", [])
                for keyword in keywords_list:
                    if keyword:  # Only create nodes for non-empty keywords
                        self.create_keyword_node(keyword)
                
                # Create relationships
                source_name = source_node.get("source", "")
                article_url = article_node.get("url", "")
                
                # Create Source -> Article relationship
                self.create_source_article_relationship(source_name, article_url)
                
                # Create Article -> Keywords relationships
                self.create_article_keyword_relationships(article_url, keywords_list)
                
                # TODO: Implement actual knowledge graph insertion logic here
                # For now, just print the extracted data
                
            print(f"\nSuccessfully processed {len(data)} articles")
            return True
            
        except Exception as e:
            print(f"Error inserting data into knowledge graph: {e}")
            return False 