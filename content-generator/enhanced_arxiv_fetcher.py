#!/usr/bin/env python3
"""
Enhanced ArXiv Paper Fetcher
Enhanced version with better recent paper search, relevance scoring, and figure generation support.
"""

import arxiv
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict, Optional
import re

class EnhancedArxivFetcher:
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
    
    def search_recent_papers(self, query="machine learning", max_results=10, days_back=7):
        """
        Search for recent papers on arXiv with enhanced filtering
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            days_back (int): Number of days to look back
            
        Returns:
            list: List of paper dictionaries
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Enhanced search queries for AI/ML papers
        ai_ml_queries = [
            f"({query})",
            "(artificial intelligence OR machine learning OR deep learning OR neural network OR transformer OR attention mechanism)",
            "(computer vision OR natural language processing OR reinforcement learning OR generative model)"
        ]
        
        all_papers = []
        
        for search_query in ai_ml_queries:
            try:
                search = arxiv.Search(
                    query=search_query,
                    max_results=max_results // len(ai_ml_queries) + 5,  # Get more to filter later
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    sort_order=arxiv.SortOrder.Descending
                )
                
                for result in search.results():
                    # Filter for relevant categories and recent papers
                    relevant_categories = ['cs.AI', 'cs.LG', 'cs.CV', 'cs.CL', 'cs.NE', 'stat.ML']
                    paper_date = result.published.replace(tzinfo=None)
                    
                    if (any(cat in result.categories for cat in relevant_categories) and 
                        paper_date >= start_date):
                        
                        paper_data = {
                            'id': result.entry_id.split('/')[-1],
                            'title': result.title,
                            'authors': [str(author) for author in result.authors],
                            'summary': result.summary,
                            'published': result.published.isoformat(),
                            'updated': result.updated.isoformat() if result.updated else None,
                            'categories': result.categories,
                            'pdf_url': result.pdf_url,
                            'entry_id': result.entry_id,
                            'relevance_score': self._calculate_relevance_score(result),
                            'category': self._map_category(result.categories)
                        }
                        all_papers.append(paper_data)
                        
            except Exception as e:
                print(f"Error searching with query '{search_query}': {e}")
                continue
        
        # Remove duplicates and sort by relevance score
        unique_papers = {}
        for paper in all_papers:
            if paper['id'] not in unique_papers:
                unique_papers[paper['id']] = paper
        
        # Sort by relevance score (higher is better)
        sorted_papers = sorted(unique_papers.values(), 
                             key=lambda x: x.get('relevance_score', 0), 
                             reverse=True)
        
        return sorted_papers[:max_results]
    
    def _calculate_relevance_score(self, result):
        """
        Calculate a relevance score for a paper based on various factors
        
        Args:
            result: arXiv search result object
            
        Returns:
            float: Relevance score (higher is better)
        """
        score = 0
        
        # Category relevance (AI/ML categories get higher scores)
        high_value_categories = ['cs.AI', 'cs.LG', 'cs.CV', 'cs.CL']
        medium_value_categories = ['cs.NE', 'stat.ML', 'cs.IR']
        
        for category in result.categories:
            if category in high_value_categories:
                score += 10
            elif category in medium_value_categories:
                score += 5
        
        # Title and abstract keyword relevance
        important_keywords = [
            'transformer', 'attention', 'neural network', 'deep learning',
            'machine learning', 'artificial intelligence', 'generative',
            'classification', 'detection', 'segmentation', 'language model',
            'computer vision', 'natural language processing', 'reinforcement learning',
            'diffusion', 'llm', 'large language model', 'multimodal', 'vision transformer'
        ]
        
        title_lower = result.title.lower()
        summary_lower = result.summary.lower()
        
        for keyword in important_keywords:
            if keyword in title_lower:
                score += 3
            elif keyword in summary_lower:
                score += 1
        
        # Recency bonus (more recent papers get slightly higher scores)
        days_old = (datetime.now() - result.published.replace(tzinfo=None)).days
        if days_old <= 1:
            score += 5
        elif days_old <= 7:
            score += 3
        elif days_old <= 30:
            score += 1
        
        # Length bonus (longer abstracts often indicate more substantial work)
        if len(result.summary) > 1000:
            score += 2
        elif len(result.summary) > 500:
            score += 1
        
        return score
    
    def _map_category(self, arxiv_categories: List[str]) -> str:
        """Map arXiv categories to blog categories."""
        category_mapping = {
            'cs.LG': 'foundation-models',  # Machine Learning
            'cs.CL': 'foundation-models',  # Computation and Language
            'cs.CV': 'basic-concepts',     # Computer Vision
            'cs.AI': 'foundation-models',  # Artificial Intelligence
            'cs.NE': 'basic-concepts',     # Neural and Evolutionary Computing
            'stat.ML': 'foundation-models', # Machine Learning (Statistics)
            'cs.RO': 'ai-applications',    # Robotics
            'cs.HC': 'ai-applications',    # Human-Computer Interaction
            'q-bio': 'ai-applications',    # Quantitative Biology
        }
        
        for cat in arxiv_categories:
            if cat in category_mapping:
                return category_mapping[cat]
        
        # Default category
        return 'basic-concepts'
    
    def search_papers_by_topic(self, topic: str, max_results: int = 5) -> List[Dict]:
        """
        Search for papers by specific topic
        
        Args:
            topic (str): Topic to search for
            max_results (int): Maximum number of results
            
        Returns:
            list: List of paper dictionaries
        """
        try:
            search = arxiv.Search(
                query=topic,
                max_results=max_results * 2,  # Get more to filter
                sort_by=arxiv.SortCriterion.Relevance,
                sort_order=arxiv.SortOrder.Descending
            )
            
            papers = []
            for result in search.results():
                # Filter for relevant categories
                relevant_categories = ['cs.AI', 'cs.LG', 'cs.CV', 'cs.CL', 'cs.NE', 'stat.ML']
                if any(cat in result.categories for cat in relevant_categories):
                    paper_data = {
                        'id': result.entry_id.split('/')[-1],
                        'title': result.title,
                        'authors': [str(author) for author in result.authors],
                        'summary': result.summary,
                        'published': result.published.isoformat(),
                        'updated': result.updated.isoformat() if result.updated else None,
                        'categories': result.categories,
                        'pdf_url': result.pdf_url,
                        'entry_id': result.entry_id,
                        'relevance_score': self._calculate_relevance_score(result),
                        'category': self._map_category(result.categories)
                    }
                    papers.append(paper_data)
                    
                    if len(papers) >= max_results:
                        break
            
            return papers
            
        except Exception as e:
            print(f"Error searching papers by topic '{topic}': {e}")
            return []
    
    def get_trending_topics(self) -> List[str]:
        """
        Get list of trending AI/ML topics for paper search
        
        Returns:
            list: List of trending topics
        """
        return [
            "large language model",
            "vision transformer", 
            "diffusion model",
            "multimodal learning",
            "reinforcement learning from human feedback",
            "few-shot learning",
            "self-supervised learning",
            "neural architecture search",
            "federated learning",
            "explainable AI",
            "adversarial robustness",
            "continual learning",
            "meta learning",
            "graph neural network",
            "attention mechanism"
        ]
    
    def save_papers_to_json(self, papers: List[Dict], filename: str):
        """Save papers to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(papers)} papers to {filename}")

def main():
    """Example usage of EnhancedArxivFetcher."""
    fetcher = EnhancedArxivFetcher()
    
    # Get recent papers
    print("Getting recent papers...")
    recent_papers = fetcher.search_recent_papers(
        query="transformer OR attention mechanism", 
        max_results=5, 
        days_back=30
    )
    fetcher.save_papers_to_json(recent_papers, 'recent_papers.json')
    
    # Search by trending topics
    print("Searching by trending topics...")
    trending_topics = fetcher.get_trending_topics()
    for topic in trending_topics[:3]:  # Test first 3 topics
        print(f"Searching for: {topic}")
        papers = fetcher.search_papers_by_topic(topic, max_results=2)
        if papers:
            print(f"Found {len(papers)} papers for {topic}")
    
    print("Done!")

if __name__ == "__main__":
    main()

