import json
from sentence_transformers import SentenceTransformer, util


class KeywordMapper:
    """
    A class for mapping and determining keywords from datasets.
    """
    
    def __init__(self):
        """
        Initialize the KeywordMapper.
        """
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def keyword_determiner(self, datasets, keyword_list):
        """
        Function to determine keywords based on datasets and keyword list.
        
        Args:
            datasets: Dictionary containing 'breitbart' and 'guardian' datasets
            keyword_list: List of keywords to process
            
        Returns:
            To be defined based on function requirements
        """
        for dataset_name, articles in datasets.items():
            for article in articles:
                # Extract content from each article and store it in a variable
                content = article.get('content', '')
               #print(content)
                
                # Call keyword_sentence_transformer to find related keywords
                
                related_keywords = self.keyword_sentence_transformer(content, keyword_list)
                print(f"Related keywords: {related_keywords}")
                print(f"Keyword list: {keyword_list}")
                
                # Replace the original keywords with the related keywords
                article['keywords'] = related_keywords
                with open('temp.txt', 'a', encoding='utf-8') as f:
                    json.dump(article, f, indent=2, ensure_ascii=False)
                    f.write(",\n")
                    #f.write(f"header: {article['title']}\n")
                    #f.write(f"keywords: {related_keywords}\n")
            
            # Save the modified articles back to their respective JSON files
            if dataset_name == 'breitbart':
                with open('new_breitbart.json', 'w', encoding='utf-8') as f:
                    json.dump(articles, f, indent=2, ensure_ascii=False)
                print(f"✓ Created new_breitbart.json with modified keywords")
            elif dataset_name == 'guardian':
                with open('new_guardian.json', 'w', encoding='utf-8') as f:
                    json.dump(articles, f, indent=2, ensure_ascii=False)
                print(f"✓ Created new_guardian.json with modified keywords")
                # Next steps will be added as we go on
    
    def keyword_sentence_transformer(self, content, keyword_list, top_k=5):
        """
        Transform content and keywords using sentence transformers to find semantically related keywords.
        
        Args:
            content: The text content to process
            keyword_list: List of keywords to process
            top_k: Number of top keywords to return (default: 5)
            
        Returns:
            List of top-k keywords that are most semantically related to the content
        """
        if not content or not keyword_list:
            return []
        
        # Encode the article content
        article_embedding = self.model.encode(content, convert_to_tensor=True)
        
        keyword_scores = []
        
        # Calculate similarity for each keyword
        for keyword in keyword_list:
            keyword_embedding = self.model.encode(keyword, convert_to_tensor=True)
            similarity = util.cos_sim(article_embedding, keyword_embedding).item()
            
            keyword_scores.append({
                'keyword': keyword,
                'similarity_score': similarity
            })
        
        # Sort by similarity score (highest first) and return top-k keywords
        keyword_scores.sort(key=lambda x: x['similarity_score'], reverse=True)
        top_keywords = keyword_scores[:top_k]
        
        return [item['keyword'] for item in top_keywords] 