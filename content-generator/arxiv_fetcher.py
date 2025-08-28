#!/usr/bin/env python3
"""
ArXiv Paper Fetcher
Fetches paper information from arXiv API for AI/ML paper blog generation.
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import time
from typing import List, Dict, Optional

class ArxivFetcher:
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.classic_papers = [
            {
                "id": "1706.03762",
                "title": "Attention Is All You Need",
                "authors": ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar", "Jakob Uszkoreit", "Llion Jones", "Aidan N. Gomez", "Lukasz Kaiser", "Illia Polosukhin"],
                "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
                "published": "2017-06-12",
                "category": "foundation-models",
                "url": "https://arxiv.org/abs/1706.03762"
            },
            {
                "id": "1207.0580",
                "title": "ImageNet Classification with Deep Convolutional Neural Networks",
                "authors": ["Alex Krizhevsky", "Ilya Sutskever", "Geoffrey E. Hinton"],
                "abstract": "We trained a large, deep convolutional neural network to classify the 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest into the 1000 different classes. On the test data, we achieved top-1 and top-5 error rates of 37.5% and 17.0% which is considerably better than the previous state-of-the-art.",
                "published": "2012-07-03",
                "category": "basic-concepts",
                "url": "https://arxiv.org/abs/1207.0580"
            },
            {
                "id": "1406.2661",
                "title": "Generative Adversarial Networks",
                "authors": ["Ian J. Goodfellow", "Jean Pouget-Abadie", "Mehdi Mirza", "Bing Xu", "David Warde-Farley", "Sherjil Ozair", "Aaron Courville", "Yoshua Bengio"],
                "abstract": "We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models: a generative model G that captures the data distribution, and a discriminative model D that estimates the probability that a sample came from the training data rather than G.",
                "published": "2014-06-10",
                "category": "generative-models",
                "url": "https://arxiv.org/abs/1406.2661"
            },
            {
                "id": "1810.04805",
                "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
                "authors": ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"],
                "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers.",
                "published": "2018-10-11",
                "category": "foundation-models",
                "url": "https://arxiv.org/abs/1810.04805"
            },
            {
                "id": "1909.11942",
                "title": "Language Models are Unsupervised Multitask Learners",
                "authors": ["Alec Radford", "Jeffrey Wu", "Rewon Child", "David Luan", "Dario Amodei", "Ilya Sutskever"],
                "abstract": "Natural language processing tasks, such as question answering, machine translation, reading comprehension, and summarization, are typically approached with supervised learning on taskspecific datasets. We demonstrate that language models begin to learn these tasks without any explicit supervision when trained on a new dataset of millions of webpages called WebText.",
                "published": "2019-02-14",
                "category": "foundation-models",
                "url": "https://arxiv.org/abs/1909.11942"
            }
        ]
    
    def get_classic_papers(self) -> List[Dict]:
        """Get the list of classic papers for initial blog content."""
        return self.classic_papers
    
    def search_papers(self, query: str, max_results: int = 10, category: str = None) -> List[Dict]:
        """
        Search for papers on arXiv.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            category: arXiv category (e.g., 'cs.LG', 'cs.CL', 'cs.CV')
        
        Returns:
            List of paper dictionaries
        """
        params = {
            'search_query': query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        if category:
            params['search_query'] = f"cat:{category} AND {query}"
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            papers = []
            
            # Define namespaces
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            for entry in root.findall('atom:entry', ns):
                paper = self._parse_entry(entry, ns)
                if paper:
                    papers.append(paper)
            
            return papers
            
        except Exception as e:
            print(f"Error fetching papers: {e}")
            return []
    
    def _parse_entry(self, entry, ns) -> Optional[Dict]:
        """Parse a single arXiv entry."""
        try:
            # Extract basic information
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', ns).text[:10]  # YYYY-MM-DD
            
            # Extract arXiv ID from URL
            arxiv_url = entry.find('atom:id', ns).text
            arxiv_id = arxiv_url.split('/')[-1]
            
            # Extract authors
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns).text
                authors.append(name)
            
            # Extract categories
            categories = []
            for category in entry.findall('atom:category', ns):
                categories.append(category.get('term'))
            
            # Map arXiv categories to blog categories
            blog_category = self._map_category(categories)
            
            return {
                'id': arxiv_id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'published': published,
                'category': blog_category,
                'url': f"https://arxiv.org/abs/{arxiv_id}",
                'arxiv_categories': categories
            }
            
        except Exception as e:
            print(f"Error parsing entry: {e}")
            return None
    
    def _map_category(self, arxiv_categories: List[str]) -> str:
        """Map arXiv categories to blog categories."""
        category_mapping = {
            'cs.LG': 'foundation-models',  # Machine Learning
            'cs.CL': 'foundation-models',  # Computation and Language
            'cs.CV': 'basic-concepts',     # Computer Vision
            'cs.AI': 'foundation-models',  # Artificial Intelligence
            'cs.NE': 'basic-concepts',     # Neural and Evolutionary Computing
            'stat.ML': 'foundation-models', # Machine Learning (Statistics)
            'cs.RO': 'applications',       # Robotics
            'cs.HC': 'applications',       # Human-Computer Interaction
            'q-bio': 'applications',       # Quantitative Biology
        }
        
        for cat in arxiv_categories:
            if cat in category_mapping:
                return category_mapping[cat]
        
        # Default category
        return 'basic-concepts'
    
    def get_recent_papers(self, days: int = 7, categories: List[str] = None) -> List[Dict]:
        """
        Get recent papers from specified categories.
        
        Args:
            days: Number of days to look back
            categories: List of arXiv categories to search
        
        Returns:
            List of recent papers
        """
        if categories is None:
            categories = ['cs.LG', 'cs.CL', 'cs.CV', 'cs.AI']
        
        all_papers = []
        
        for category in categories:
            query = f"cat:{category}"
            papers = self.search_papers(query, max_results=20)
            all_papers.extend(papers)
            time.sleep(1)  # Be respectful to arXiv API
        
        # Sort by publication date (most recent first)
        all_papers.sort(key=lambda x: x['published'], reverse=True)
        
        return all_papers[:10]  # Return top 10 most recent
    
    def save_papers_to_json(self, papers: List[Dict], filename: str):
        """Save papers to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(papers)} papers to {filename}")

def main():
    """Example usage of ArxivFetcher."""
    fetcher = ArxivFetcher()
    
    # Get classic papers
    print("Getting classic papers...")
    classic_papers = fetcher.get_classic_papers()
    fetcher.save_papers_to_json(classic_papers, 'classic_papers.json')
    
    # Search for recent transformer papers
    print("Searching for recent transformer papers...")
    recent_papers = fetcher.search_papers("transformer attention", max_results=5, category="cs.LG")
    fetcher.save_papers_to_json(recent_papers, 'recent_papers.json')
    
    print("Done!")

if __name__ == "__main__":
    main()

