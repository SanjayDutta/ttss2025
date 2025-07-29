from actions.db_actions.mongo_setup import db_create, initialize_collections

def run_initialization(app):
    """
    Run the initialization process for the application.
    This function is called when the application starts.
    """
    print("Running initialization...")
    
    # Initialize MongoDB database
    print("Initializing MongoDB database...")
    db_config = db_create()
    
    if db_config:
        print(f"MongoDB database '{db_config['db_name']}' initialized successfully")
        # Store database configuration in app config for later use
        app.config['MONGO_CONFIG'] = db_config
        
        # Initialize collections and upload data
        print("Initializing collections and uploading data...")
        collections_result = initialize_collections()
        
        if collections_result:
            print("Collections initialized and data uploaded successfully")
        else:
            print("Failed to initialize collections or upload data")
    else:
        print("Failed to initialize MongoDB database")
    
    # Add any other initialization logic here
    # For example:
    # - Other database connections
    # - Configuration loading
    # - Service initialization 