from flask import Blueprint, request, jsonify, send_file
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import glob
from lxml import etree
import requests

# Load environment variables
load_dotenv()

main = Blueprint('main', __name__)

@main.route("/")
def hello_world():
    return "Hello, World!"

@main.route("/health")
def health_check():
    return {"status": "healthy", "message": "Flask application is running"}

@main.route("/fetch_articles_keywords", methods=['POST'])
def fetch_articles_keywords():
    """
    Fetch articles from MongoDB based on provided keywords
    Expected JSON payload: {"keywords": ["keyword1", "keyword2", ...]}
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'keywords' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Keywords are required in request body'
            }), 400
        
        keywords = data['keywords']
        
        if not isinstance(keywords, list) or len(keywords) == 0:
            return jsonify({
                'status': 'error',
                'message': 'Keywords must be a non-empty list'
            }), 400
        
        # Create a normalized keywords string for filenames (first two keywords, capitalized, underscores)
        def keywords_filename(keywords):
            return '_'.join([str(k).capitalize() for k in keywords[:2]])

        # Check if HTML file with same keywords already exists
        # Use absolute path to avoid app directory context issues
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        xml_folder = os.path.join(base_dir, "fetched_XML_kw_File")
        existing_html_file = None
        keywords_str = keywords_filename(keywords)
        if os.path.exists(xml_folder):
            pattern = f"articles_search_{keywords_str}.html"
            matching_files = glob.glob(os.path.join(xml_folder, pattern))
            if matching_files:
                existing_html_file = matching_files[0]
                print(f"Found existing HTML file with same keywords: {existing_html_file}")
        
        # If existing HTML file found, return it directly
        if existing_html_file:
            print(f"Returning cached HTML file: {existing_html_file}")
            if os.path.exists(existing_html_file):
                return send_file(existing_html_file, mimetype='text/html')
            else:
                print(f"HTML file not found at expected path: {existing_html_file}")
                # Continue to MongoDB query if file doesn't exist
        
        # If no existing HTML file found, query MongoDB
        print("No existing HTML file found, querying MongoDB...")
        if not existing_html_file:
            # Get MongoDB configuration from environment variables
            mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
            db_name = os.getenv('MONGO_DB_NAME', 'flask_app_db')
            
            # Create MongoDB client
            client = MongoClient(mongo_uri)
            
            # Get database and collection
            db = client[db_name]
            articles_collection = db.articles

            #run the query twice, once for guardian and once for breitbart
            guardian_articles = list(articles_collection.find({'source': 'The Guardian', 'bias_score': {'$ne': "N/A"}, 'keywords': {'$in': keywords}}, {'_id': 0}).limit(50))
            breitbart_articles = list(articles_collection.find({'source': 'Breitbart News Network', 'bias_score': {'$ne': "N/A"}, 'keywords': {'$in': keywords}}, {'_id': 0}).limit(50))
            
            #combine the two lists
            articles = guardian_articles + breitbart_articles

            guardian_content = ""
            breitbart_content = ""
            for guardian_article in guardian_articles:
                guardian_content += "\n\n Article " +":\n" + guardian_article.get("content")
            for breitbart_article in breitbart_articles:
                breitbart_content += "\n\nArticle " + ":\n" + breitbart_article.get("content")

            with open("guardian_content.txt", "w") as f:
                f.write(guardian_content)
            with open("breitbart_content.txt", "w") as f:
                f.write(breitbart_content)
            
            #search only in keywords field, where keywords is a list
            '''search_query = {
                'keywords': {'$in': keywords},

            }
            
            # Execute query with limit to prevent overwhelming response
            articles = list(articles_collection.find(search_query, {'_id': 0}).limit(50))
            guardian_content = ""
            breitbart_content = ""
            
            for article in articles:
                guardian_articles = []
                breitbart_articles = []
                if article.get('source') == 'The Guardian':
                    guardian_articles.append(article.get("content"))                    
                else:
                    breitbart_articles.append(article.get("content"))


                if guardian_articles:
                    for article in (guardian_articles):
                       guardian_content += "\n\n Article " +":\n" + article  
                    
                if breitbart_articles:             
                    for article in breitbart_articles:                        
                        breitbart_content += "\n\nArticle " + ":\n" + article'''

            # Close MongoDB connection
            client.close()
            
            #convert all keywords into a string
            keywords_string = ", ".join(keywords)

            # Send request for Guardian content for LLM Analysis to Llama3.2
            if guardian_content:
                guardian_content_limited =""
                #collect first 20 content from guardian_articles
                for guardian_article in guardian_articles:
                    guardian_content_limited += "\n\n Article " +":\n" + guardian_article.get("title") + "\n"
                llama_response =""
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "llama3.2:3b", "prompt": "You are a helpful assistant with expertise in understanding political landscape. The user will provide you multiple articles.Tell me, what the general view is based on the articles, the sentiment behind the all news article, as well as the general bias associated with it -like left/leanleft/neutral/lean right/right and give one sentence reasoning behind it.Also word limit is 150. Also use <b></b> to put worlds which are usually between ****\n\nKeywords: " + keywords_string +"\n"+guardian_content_limited, "stream": False}
                )
                llama_response = response.json()['response']
                
            # Send request for Breitbart content for LLM Analysis to Llama3.2
            if breitbart_content:
                # Limit Breitbart content to first 15000 words
                breitbart_words = breitbart_content.split()
                breitbart_content_limited = ' '.join(breitbart_words[:10000])
                breitbart_llama_response =""
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "llama3.2:3b", "prompt": "You are a helpful assistant with expertise in understanding political landscape. The user will provide you multiple articles.Tell me, what the general view is based on the articles, the sentiment behind the all news article, as well as the general bias associated with it -like left/leanleft/neutral/lean right/right and give one sentence reasoning behind it.Also word limit is 150. Also use <b></b> to put worlds which are usually between ****\n\nKeywords: " + keywords_string +"\n"+breitbart_content_limited, "stream": False}
                )
                breitbart_llama_response = response.json()['response']
                
               

        
        
        # Write results to XML file and generate HTML
        html_file_path = None
        if articles:
            # Create XML structure
            root = ET.Element("articles_search_results")
            
            # Add metadata
            metadata = ET.SubElement(root, "metadata")
            ET.SubElement(metadata, "search_timestamp").text = datetime.now().isoformat()
            ET.SubElement(metadata, "keywords_searched").text = ", ".join(keywords)
            ET.SubElement(metadata, "total_articles_found").text = str(len(articles))
            ET.SubElement(metadata, "keywords_string").text = keywords_string
            
            '''# Add Guardian analysis if available
            if 'guardian_analysis' in locals() and guardian_analysis and 'choices' in guardian_analysis and len(guardian_analysis['choices']) > 0:
                guardian_content_analysis = guardian_analysis['choices'][0]['message']['content']
                #convert llama response to string
                ET.SubElement(metadata, "guardian_analysis").text = llama_response
                #ET.SubElement(metadata, "guardian_analysis").text = guardian_content_analysis
            
            # Add Breitbart analysis if available
            if 'breitbart_analysis' in locals() and breitbart_analysis and 'choices' in breitbart_analysis and len(breitbart_analysis['choices']) > 0:
                breitbart_content = breitbart_analysis['choices'][0]['message']['content']
                #ET.SubElement(metadata, "breitbart_analysis").text = breitbart_content 
                ET.SubElement(metadata, "breitbart_analysis").text = breitbart_llama_response'''

            if llama_response:
                ET.SubElement(metadata, "guardian_analysis").text = llama_response
                
            # Add Breitbart analysis if available
            if breitbart_llama_response:
                ET.SubElement(metadata, "breitbart_analysis").text = breitbart_llama_response






            # Add articles
            articles_element = ET.SubElement(root, "articles")
            
            for article in articles:
                article_elem = ET.SubElement(articles_element, "article")
                
                # Add only the specified fields
                ET.SubElement(article_elem, "url").text = article.get('url', '')
                ET.SubElement(article_elem, "title").text = article.get('title', '')
                ET.SubElement(article_elem, "author").text = article.get('author', '')
                ET.SubElement(article_elem, "date").text = article.get('date', '')
                ET.SubElement(article_elem, "source").text = article.get('source', '')
                
                # Add bias information if available
                if 'bias_score' in article:
                    ET.SubElement(article_elem, "bias_score").text = str(article.get('bias_score', ''))
                if 'bias_analysis' in article:
                    ET.SubElement(article_elem, "bias_analysis").text = article.get('bias_analysis', '')
            
            # Create pretty XML string
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            
            # Create directory if it doesn't exist
            # Use the same absolute path as defined above
            if not os.path.exists(xml_folder):
                os.makedirs(xml_folder)
                print(f"Created directory: {xml_folder}")
            
            # Generate filename with timestamp
            filename = f"articles_search_{keywords_str}.xml"
            
            # Create full file path
            file_path = os.path.join(xml_folder, filename)
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            
            print(f"Search results written to XML file: {file_path}")

            # Generate XSLT file if not present
            xslt_path = os.path.join(xml_folder, 'articles_to_html.xslt')
            if not os.path.exists(xslt_path):
                xslt_content = '''<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" indent="yes"/>
  <xsl:template match="/">
    <html>
      <head>
        <title>Articles Search Results</title>
        <style>
          table, th, td { border: 1px solid black; border-collapse: collapse; }
          th, td { padding: 8px; }
          .bias-analysis { max-width: 300px; word-wrap: break-word; }
          .url-cell { max-width: 200px; word-wrap: break-word; }
        </style>
      </head>
      <body>
        <h2>Articles Search Results</h2>
        <xsl:for-each select="articles_search_results/metadata">
          <div><b>Search Timestamp:</b> <xsl:value-of select="search_timestamp"/></div>
          <div><b>Keywords Searched:</b> <xsl:value-of select="keywords_searched"/></div>
          <div><b>Total Articles Found:</b> <xsl:value-of select="total_articles_found"/></div>
          <xsl:if test="guardian_analysis">
            <div><b>Guardian AI Analysis:</b> <xsl:value-of select="guardian_analysis"/></div>
          </xsl:if>
          <xsl:if test="breitbart_analysis">
            <div><b>Breitbart AI Analysis:</b> <xsl:value-of select="breitbart_analysis"/></div>
          </xsl:if>
        </xsl:for-each>
        <table>
          <tr>
            <th >Title</th>
            <th>Author</th>
            <th>Source</th>
            <th style="width: 15%;">Date</th>
            <th style="width: 7%;">Bias Score</th>
            <th style="width: 50%;">Bias Analysis</th>
          </tr>
          <xsl:for-each select="articles_search_results/articles/article">
            <tr>
              <td><a href="{url}" target="_blank"><xsl:value-of select="title"/></a></td>
              <td><xsl:value-of select="author"/></td>
              <td><xsl:value-of select="source"/></td>
              <td><xsl:value-of select="date"/></td>
              <td><xsl:value-of select="bias_score"/></td>
              <td class="bias-analysis"><xsl:value-of select="bias_analysis"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
'''
                with open(xslt_path, 'w', encoding='utf-8') as xslt_file:
                    xslt_file.write(xslt_content)
            # Convert XML to HTML using XSLT
            try:
                dom = etree.parse(file_path)
                xslt = etree.parse(xslt_path)
                transform = etree.XSLT(xslt)
                html_dom = transform(dom)
                html_file_path = file_path.replace('.xml', '.html')
                with open(html_file_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(str(html_dom))
                print(f"HTML file created: {html_file_path}")
                print(f"HTML file exists after creation: {os.path.exists(html_file_path)}")
            except Exception as e:
                print(f"Error converting XML to HTML: {e}")
                html_file_path = None

        # Return the HTML file that was just created
        if html_file_path and os.path.exists(html_file_path):
            return send_file(html_file_path, mimetype='text/html')
        else:
            # Fallback: return a simple HTML response if no HTML file was created
            return f'''
            <html>
            <head><title>Search Results</title></head>
            <body>
            <h2>Search Results</h2>
            <p>Found {len(articles)} articles matching keywords: {keywords}</p>
            <p>No HTML file was generated. Please check the server logs.</p>
            <p>HTML file path: {html_file_path}</p>
            <p>File exists: {os.path.exists(html_file_path) if html_file_path else "No path"}</p>
            </body>
            </html>
            ''', 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching articles: {str(e)}'
        }), 500 