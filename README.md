# TTSS2025 Project - News Focus Analysis

## Project Overview
NewsFocus aims to provide a structured and comparative analysis of news coverage from  ideologically diverse outlets by leveraging knowledge representation tools and modern 
large-language models. 
The core objectives of the project are: 
1. To collect news articles from various sources using public APIs or web scraping. 
2. To process articles via annotating each article with key attributes, including: 
    <br>2.1. Genre classification 
    <br>2.2. Political bias rating 
    <br>2.3. Expert opinion consolidation  
3. To enable easy user access/consumption through a UI friendly dashboard, and  LLM-generated summary and focus report 
 
The processed data is modelled into a knowledge graph to support structured analysis 
and visualisation. This enables the system to answer – Which topics are most frequently 
reported by each outlet, which topics are most prevalent in various segments of the 
political spectrum and how many articles are written per genre by each outlet. By 
combining the semantic capabilities of Large Language Models (LLMs) with relational 
insights of graph databases, NewsFocus facilitates the detection of media bias and 
ideological framing across the political spectrum. 
 


## Directory Structure

```
ttss2025/
├── 📄 README.md                           # Project documentation
├── 📄 .gitignore                          # Git ignore rules
│
├── 📁 access/                             # Main application directory
│   ├── 📁 Backend_Services/              # Backend API and services
│   │   ├── 📁 actions/                   # Database actions
│   │   │   ├── 📁 db_actions/
│   │   │   │   └── mongo_setup.py        # MongoDB configuration
│   │   │   └── __init__.py
│   │   ├── 📁 app/
│   │   │   └── __init__.py
│   │   ├── 📁 routes/                    # API routes
│   │   │   ├── graph_operations.py       # Knowledge graph operations
│   │   │   ├── main.py                   # Main API routes
│   │   │   └── __init__.py
│   │   ├── 📁 startup/                   # Application startup
│   │   │   ├── initializer.py            # App initialization
│   │   │   └── __init__.py
│   │   ├── 📁 data/                      # Data storage
│   │   │   └── articles.json             # Article data
│   │   ├── 📁 fetched_XML_kw_File/       # XML and HTML files
│   │   │   ├── articles_search_Donald trump.html
│   │   │   ├── articles_search_Donald trump.xml
│   │   │   └── articles_to_html.xslt     # XSLT transformation
│   │   ├── 📄 requirements.txt           # Python dependencies
│   │   ├── 📄 run.py                     # Application entry point
│   │   ├── 📄 breitbart_content.txt      # Extracted Breitbart content
│   │   ├── 📄 guardian_content_analysis.txt
│   │   ├── 📄 guardian_content_limited.txt
│   │   ├── 📄 guardian_content.txt       # Extracted Guardian content
│   │   ├── 📄 llama_analysis.txt         # LLM analysis results
│   │   └── 📄 prompt                     # AI prompt templates
│   │
│   └── 📁 frontend/                      # Vue.js frontend application
│       ├── 📁 assets/                    # Static assets
│       │   └── 📁 css/
│       │       └── global.css            # Global styles
│       ├── 📁 components/                # Vue components
│       │   ├── Documentation.vue         # Documentation component
│       │   ├── KeywordFinder.vue         # Keyword search component
│       │   ├── KnowledgeGraph.vue        # Graph visualization
│       │   ├── NewsSourceInfo.vue        # News source information
│       │   └── NodePopup.vue             # Node interaction popup
│       ├── 📁 pages/                     # Application pages
│       │   ├── graph-test.vue            # Graph testing page
│       │   ├── graph.vue                 # Main graph page
│       │   ├── home.vue                  # Home page
│       │   ├── index.vue                 # Index page
│       │   └── test.vue                  # Testing page
│       ├── 📁 plugins/                   # Vue plugins
│       │   └── bootstrap.client.js       # Bootstrap integration
│       ├── 📁 public/                    # Public assets
│       │   ├── favicon.ico
│       │   ├── robots.txt
│       │   └── sample.html
│       ├── 📄 nuxt.config.js             # Nuxt.js configuration
│       ├── 📄 package.json               # Node.js dependencies
│       ├── 📄 package-lock.json
│       └── 📄 README.md                  # Frontend documentation
│
├── 📁 collect/                           # Data collection modules
│   ├── 📁 extract_breitbart/            # Breitbart data extraction
│   │   ├── 📄 breitbart_sitemap.xml     # Sitemap data
│   │   ├── 📄 daily_sitemaps.txt        # Daily sitemap URLs
│   │   ├── 📄 extracted_content.txt     # Extracted content
│   │   ├── 📄 fetch_content.py          # Content fetching script
│   │   ├── 📄 fetch_contentURL.py       # URL fetching script
│   │   ├── 📄 fetch_sitemaps.py         # Sitemap fetching script
│   │   ├── 📄 requirements.txt          # Python dependencies
│   │   ├── 📄 result.json               # Extraction results
│   │   ├── 📄 sample_result.json        # Sample data
│   │   └── 📁 venv/                     # Virtual environment
│   │
│   └── 📁 extract_guardian/             # Guardian data extraction
│       ├── 📄 app.py                     # Main extraction app
│       ├── 📄 bias_analysis.py          # Bias analysis script
│       ├── 📄 fetch_articles.py         # Article fetching script
│       ├── 📄 filter.py                 # Data filtering script
│       ├── 📄 requirements.txt          # Python dependencies
│       ├── 📄 README.md                 # Guardian extraction docs
│       ├── 📁 data/                     # Guardian article data
│       │   ├── guardian_articles_page_2024_06_25_2024_01_09.json
│       │   ├── guardian_articles_page_2024_12_19_2024_06_26.json
│       │   └── guardian_articles_page_2025_06_22_2024_12_20.json
│       ├── 📁 filtered_data/            # Filtered article data
│       │   └── guardian_articles_with_bias_analysis_set1.json
│       ├── 📁 filtered_daterange_data/  # Date-filtered data
│       │   └── guardian_articles_page_2025_06_22_2024_12_20.json
│       └── 📄 filtered_articles_part*.json  # Multiple filtered datasets
│
└─── 📁 prepare/                           # Data preparation modules
    ├── 📁 keyword_consolidator/         # Keyword consolidation tool
    │   ├── 📄 app.py                     # Main consolidation app
    │   ├── 📄 keyword_mapper.py         # Keyword mapping logic
    │   ├── 📄 requirements.txt          # Python dependencies
    │   ├── 📄 breitbart.json            # Breitbart keywords
    │   ├── 📄 guardian.json             # Guardian keywords
    │   ├── 📄 keywords.json             # Consolidated keywords
    │   ├── 📄 temp.txt                  # Temporary data
    │   └── 📁 venv/                     # Virtual environment
    │
    └── 📁 kg_dataloader/                # Knowledge graph data loader
        ├── 📄 app.py                     # Main loader app
        ├── 📄 kg_operation.py           # Graph operations
        ├── 📄 json_reader.py            # JSON data reader
        ├── 📄 extract_breitbart.py      # Breitbart data extraction
        ├── 📄 extract_guardian.py       # Guardian data extraction
        ├── 📄 check_breitbart_data.py   # Data validation
        ├── 📄 compare_json_structure.py # Structure comparison
        ├── 📄 requirements.txt          # Python dependencies
        ├── 📄 breitbart.json            # Breitbart processed data
        ├── 📄 guardian.json             # Guardian processed data
        ├── 📄 result.json               # Processing results
        └── 📁 venv/                     # Virtual environment



```

## Project Components

### 1. Data Collection (`collect/`)
- **Breitbart Extraction**: Web scraping and content extraction from Breitbart news
- **Guardian Extraction**: API-based article collection from The Guardian with bias analysis

### 2. Data Preparation (`prepare/`)
- **Keyword Consolidator**: Merges and standardizes keywords from different sources
- **KG Data Loader**: Prepares data for knowledge graph construction

### 3. Application (`access/`)
- **Backend Services**: Python Flask API with MongoDB integration
- **Frontend**: Vue.js/Nuxt.js application with interactive knowledge graph visualization

### 4. Documentation (`documents/`)
- Project reports, methodology, and academic documentation

## Technology Stack

- **Backend**: Python, Flask, MongoDB
- **Frontend**: Vue.js, Nuxt.js, Bootstrap
- **Data Processing**: Python scripts for web scraping and analysis
- **Visualization**: Interactive knowledge graphs
- **AI/ML**: LLM analysis for bias detection

## Project Setup

To successfully run the project, there are requirements which need to be fulfilled.

**Installation of Python (Flask) and NodeJS (NPM and NuxtJS)**
Our application is based on Python and the Flask Framework. As well as for the frontend application, it relies on NodeJS. 

**API KEY for The Guardian API**
Since the project relies on The Guardian API to collect the respective articles, it is required to procure an API key to successfully fetch the articles from the Guardian, especially for the Collect Phase. An API key for The Guardian can be found here - The Guardian Open Platform

**API Key for AllSides**
For bias-rating and bias-analysis, an API key is required from AllSides. Since the platform only allows making these API calls from their website, one needs to visit "Developer Tools" in the respective browsers, to fetch the API key from the "Networks Tab". Please visit – AllSides Bias Checker, to make an API call and check the Networks Tab for the API Key. [NOTE: For the sake of simplicity and free access for anyone, an API key is already made available in this project, especially in places where API calls are being made to AllSides]

**Llama 3.2 Setup Using Ollama**
Our application relies on Llama3.2:1b for various large-language-model features (like LLM-analysis and source-analysis). For this, one shall require Ollama installed in their system. Please visit Ollama to download and run the version-specific installer and then open the terminal, run the command "ollama pull llama3.2:1b" to download llama3.2:1b.

**Neo4j Knowledge Graph Database**
For data visualisation, our application requires quick reading of data. This is implemented through Neo4J. Our project already provides the script to load data into a Neo4j database (i.e. prepare/kg_dataloader/app.py). Therefore, please install Neo4j and create a database to successfully run the project. After which, please fill out the .env environment file in the aforementioned directory and run the app.py file to load the articles in the Neo4j database.

**MongoDB NoSQL Database**
Our application also relies on MongoDB, especially to find articles which incorporate a user-specified keyword. Please install MongoDB and upload the required datasets (e.g. using Compass)

## Getting Started

**Step 1: Fetching and Assigning Bias Rating to Articles**

1. Visit the directory `/extract_breitbart`
2. Create and activate a Python virtual environment and install all the requirements
3. In `fetch_sitemaps.py`, insert the start and end dates (lines no. 63 and 64). This date range represents all the articles which were published within this date range and will be fetched accordingly.
4. Run the `fetch_contentURL.py`
5. It will generate the `result.json`, which will contain all the articles and the associated bias ratings from Breitbart News

6. Next, visit the directory `/extract_guardian`
7. Create and activate a Python virtual environment and install all the requirements
8. Same as earlier, in `fetch_articles.py`, insert the from and to dates (lines no. 96 and 97). 
9. Run the `fetch_articles.py`, followed by running the `bias_analysis.py` file.
10. After running the scripts, the `guardian_articles_with_bias_analysis.json` file will be generated, which will contain all the articles and the associated bias ratings from The Guardian. 

**Step 2: Keyword Consolidator** 

1. Visit the directory `/extract_breitbart`
2. Create and activate a Python virtual environment and install all the requirements
3. Copy the contents of `result.json` into `keyword_consolidator/breitbart.json` and `guardian_articles_with_bias_analysis.json` into `keyword_consolidator/guardian.json`
4. Then run the application `keyword_consolidator/app.py`
5. Two JSON files will be generated `new_guardian.json` and `new_breitbart.json`.

**Step 3: Data loading in Neo4J Knowledge Graph**

1. Visit the directory `/kg_dataloader`
2. Create and activate a Python virtual environment and install all the requirements
3. Copy the contents of `new_guardian.json` and `new_breitbart.json` into `breitbart.json` and `guardian.json`
4. In the `.env` environment file, fill out the necessary details.
5. Run the application `app.py` twice, once when the environment variable `NEWS_FILEJSON=breitbart.json` and once when `NEWS_FILEJSON=guardian.json`
6. This will result in the creation of a Neo4j knowledge graph, depicting the relation between the news articles, their sources and the keywords.

**Step 4: Running Ollama**

1. Run Ollama and keep it running in the background
2. Also, please ensure Llama3.2 is downloaded.

**Step 5: Running Our Application**

1. Visit the directory `/access/frontend`
2. Install the necessary npm dependencies
3. Run the frontend via the terminal by writing the command `npm run dev`

4. Visit the directory `/access/Backend_Services`
5. Create and activate a Python virtual environment and install all the requirements
6. Fill out the necessary details in the `.env` environment file
7. Use the command `flask run` to start the backend services.

## Note
This project is part of the Text Technology course (TTSS2025) at the University of Stuttgart, focusing on media bias analysis and knowledge graph construction.
