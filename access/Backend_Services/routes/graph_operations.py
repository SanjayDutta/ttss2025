from flask import Blueprint, jsonify, current_app
from neo4j import GraphDatabase
import os

# Create blueprint for graph operations
graph_operations = Blueprint('graph_operations', __name__)

@graph_operations.route('/graph_test', methods=['GET'])
def graph_test():
    """
    Test endpoint for graph operations
    """
    try:
        return jsonify({
            'status': 'success',
            'message': 'Graph operations endpoint is working!',
            'endpoint': '/graph_test',
            'method': 'GET'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error in graph test endpoint: {str(e)}'
        }), 500

@graph_operations.route('/graph_data', methods=['GET'])
def get_graph_data():
    """
    Get all nodes and edges from Neo4j database
    """
    try:
        # Get Neo4j configuration from environment variables
        neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        neo4j_username = os.getenv('NEO4J_USERNAME', 'neo4j')
        neo4j_password = os.getenv('NEO4J_PASSWORD', 'your_password')
        neo4j_database = os.getenv('NEO4J_DATABASE', 'neo4j')
        
        print(f"Connecting to Neo4j: {neo4j_uri}")
        print(f"Database: {neo4j_database}")
        
        # Create Neo4j driver
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
        
        # Test connection first
        with driver.session(database=neo4j_database) as session:
            # Test connection
            result = session.run("RETURN 1 as test")
            test_value = result.single()["test"]
            print(f"Connection test successful: {test_value}")
            
            # Get total node count
            node_count_result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = node_count_result.single()["count"]
            print(f"Total nodes in database: {total_nodes}")
            
            # Get total relationship count
            rel_count_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            total_rels = rel_count_result.single()["count"]
            print(f"Total relationships in database: {total_rels}")
            
            # Query to get all nodes and relationships
            result = session.run("""
                MATCH (n)-[r]->(m)
                RETURN n, r, m 
            """)
            
            nodes = []
            edges = []
            seen = set()
            
            for record in result:
                # Process nodes
                for node in [record["n"], record["m"]]:
                    if node.id not in seen:
                        nodes.append({
                            "id": node.id, 
                            "label": list(node.labels)[0] if node.labels else "Unknown", 
                            "properties": dict(node)
                        })
                        seen.add(node.id)
                
                # Process relationships
                rel = record["r"]
                edges.append({
                    "source": rel.start_node.id,
                    "target": rel.end_node.id,
                    "type": rel.type,
                    "properties": dict(rel)
                })
            
            # Close the driver
            driver.close()
            
            return jsonify({
                "status": "success",
                "nodes": nodes,
                "edges": edges,
                "node_count": len(nodes),
                "edge_count": len(edges),
                "total_nodes_in_db": total_nodes,
                "total_relationships_in_db": total_rels,
                "connection_info": {
                    "uri": neo4j_uri,
                    "database": neo4j_database
                }
            }), 200
            
    except Exception as e:
        print(f"Neo4j error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving graph data: {str(e)}'
        }), 500 