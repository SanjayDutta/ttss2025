from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})
    
    # Basic configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Flask REST API"
    app.config["API_VERSION"] = "1.0.0"
    
    # Import and register blueprints
    from routes.main import main as MainBlueprint
    from routes.graph_operations import graph_operations as GraphOperationsBlueprint
    
    app.register_blueprint(MainBlueprint)
    app.register_blueprint(GraphOperationsBlueprint)
    
    # Run initialization if needed
    from startup.initializer import run_initialization
    run_initialization(app)
    
    return app 