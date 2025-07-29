"""
MongoDB setup and initialization module
"""
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json



# Load environment variables from .env file
load_dotenv()

def db_create():
    """
    Create a database for MongoDB
    """
    try:
        # Get MongoDB configuration from environment variables
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        db_name = os.getenv('MONGO_DB_NAME', 'flask_app_db')
        
        print(f"Creating database: {db_name}")
        print(f"Using MongoDB URI: {mongo_uri}")
        
        # Import and use pymongo to create the database
       
        
        # Create MongoDB client with proper SSL configuration for Atlas
        #client = MongoClient(mongo_uri, 
         #                  server_api=ServerApi('1'),
         #                  tls=True,
         #                  tlsAllowInvalidCertificates=True,
         #                  tlsAllowInvalidHostnames=True)
        client = MongoClient(mongo_uri)
        # Test the connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Get or create the database
        db = client[db_name]
        
        # Create a test collection to ensure the database is created
        test_collection = db.test_collection
        test_collection.insert_one({"test": "database_created", "timestamp": "2025-07-13"})
        print(f"Test document inserted into {db_name}")
        
        # Clean up test document
        test_collection.delete_one({"test": "database_created"})
        print("Test document cleaned up")
        
        return {
            'uri': mongo_uri,
            'db_name': db_name,
            'client': client,
            'db': db,
            'status': 'connected'
        }
        
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        return None

def setup_mongodb():
    """
    Setup MongoDB connection and initialize database
    """
    print("Setting up MongoDB connection...")
    # Add MongoDB setup logic here
    pass

def initialize_collections():
    """
    Initialize MongoDB collections and upload data from JSON files
    """
    try:
        print("Initializing MongoDB collections...")
        
        # Get database connection from the global context
        # This assumes db_create() has been called and the database is available
        
        
        # Get MongoDB configuration from environment variables
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        db_name = os.getenv('MONGO_DB_NAME', 'flask_app_db')
        
        # Create MongoDB client
       #client = MongoClient(mongo_uri, 
        #                   server_api=ServerApi('1'),
        #                   tls=True,
        #                   tlsAllowInvalidCertificates=True,
        #                   tlsAllowInvalidHostnames=True)
        client = MongoClient(mongo_uri)
        
        # Get database
        db = client[db_name]
        
        # Create articles collection
        articles_collection = db.articles
        
        # Check if articles collection already has data
        if articles_collection.count_documents({}) > 0:
            print("Articles collection already contains data. Skipping upload.")
            return True
        
        # Read articles data from JSON file
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'articles.json')
        
        if not os.path.exists(json_file_path):
            print(f"Articles JSON file not found at: {json_file_path}")
            return False
        
        with open(json_file_path, 'r', encoding='utf-8') as file:
            articles_data = json.load(file)
        
        print(f"Found {len(articles_data)} articles to upload")
        
        # Insert articles into MongoDB
        if articles_data:
            result = articles_collection.insert_many(articles_data)
            print(f"Successfully uploaded {len(result.inserted_ids)} articles to MongoDB")
            
            # Create indexes for better performance
            articles_collection.create_index("title")
            articles_collection.create_index("author")
            articles_collection.create_index("category")
            articles_collection.create_index("tags")
            print("Created indexes on articles collection")
            
            return True
        else:
            print("No articles data found in JSON file")
            return False
            
    except Exception as e:
        print(f"Error initializing collections: {str(e)}")
        return False

def test_connection():
    """
    Test MongoDB connection
    """
    print("Testing MongoDB connection...")
    # Add connection test logic here
    pass 