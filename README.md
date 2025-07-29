# TTSS2025 Project - News Focus Analysis

## Project Overview
This project focuses on analyzing news content from different sources (Breitbart and The Guardian) to understand media bias and create knowledge graphs for text technology research.

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
│   │   ├── 📁 app/
│   │   ├── 📁 routes/                    # API routes
│   │   │   ├── graph_operations.py       # Knowledge graph operations
│   │   │   ├── main.py                   # Main API routes
│   │   ├── 📁 startup/                   # Application startup
│   │   │   ├── initializer.py            # App initialization
│   │   ├── 📁 data/                      # Data storage
│   │   │   └── articles.json             # Article data
│   │   ├── 📁 fetched_XML_kw_File/       # XML and HTML files
│   │   │   ├── articles_search_Donald trump.html
│   │   │   ├── articles_search_Donald trump.xml
│   │   │   └── articles_to_html.xslt     # XSLT transformation
│   │   ├── 📄 requirements.txt           # Python dependencies
│   │   ├── 📄 run.py                     # Application entry point
│   │
│   └── 📁 frontend/                      # Vue.js frontend application
│       ├── 📁 assets/                    # Static assets
│       ├── 📁 components/                # Vue components
│       │   ├── Documentation.vue         # Documentation component
│       │   ├── KeywordFinder.vue         # Keyword search component
│       │   ├── KnowledgeGraph.vue        # Graph visualization
│       │   ├── NewsSourceInfo.vue        # News source information
│       │   └── NodePopup.vue             # Node interaction popup
│       ├── 📁 pages/                     # Application pages
│       │   ├── index.vue                 # Index page
│       ├── 📁 plugins/                   # Vue plugins
│       ├── 📁 public/                    # Public assets
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
│   │   └── 📁 venv/                     # Virtual environment
│   │
│   └── 📁 extract_guardian/             # Guardian data extraction
│       ├── 📄 bias_analysis.py          # Bias analysis script
│       ├── 📄 fetch_articles.py         # Article fetching script
│       ├── 📄 requirements.txt          # Python dependencies
│       └── 📄 guardian_articles.json  # Multiple filtered datasets
│
├── 📁 prepare/                           # Data preparation modules
│   ├── 📁 keyword_consolidator/         # Keyword consolidation tool
│   │   ├── 📄 app.py                     # Main consolidation app
│   │   ├── 📄 keyword_mapper.py         # Keyword mapping logic
│   │   ├── 📄 requirements.txt          # Python dependencies
│   │   ├── 📄 breitbart.json            # Breitbart keywords
│   │   ├── 📄 guardian.json             # Guardian keywords
│   │   ├── 📄 keywords.json             # Consolidated keywords
│   │   └── 📁 venv/                     # Virtual environment
│   │
│   └── 📁 kg_dataloader/                # Knowledge graph data loader
│       ├── 📄 app.py                     # Main loader app
│       ├── 📄 kg_operation.py           # Graph operations
│       ├── 📄 json_reader.py            # JSON data reader
│       ├── 📄 extract_breitbart.py      # Breitbart data extraction
│       ├── 📄 extract_guardian.py       # Guardian data extraction
│       ├── 📄 requirements.txt          # Python dependencies
│       ├── 📄 breitbart.json            # Breitbart processed data
│       ├── 📄 guardian.json             # Guardian processed data
│       ├── 📄 result.json               # Processing results
│       └── 📁 venv/                     # Virtual environment
│
├── 📁 documents/                         # Project documentation
    ├── 📄 NewsFocus_TTSS2025.pdf        # Main project document
    ├── 📄 NewsFocus.pdf                 # Project overview
    └── 📄 Text Technology.docx          # Course documentation


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

## Getting Started

1. Set up virtual environments in each Python module
2. Install dependencies from respective `requirements.txt` files
3. Configure MongoDB connection in backend services
4. Run the data collection scripts
5. Start the backend API and frontend application

## Note
This project is part of the Text Technology course (TTSS2025) at the University of Stuttgart, focusing on media bias analysis and knowledge graph construction.
