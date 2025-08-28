#!/usr/bin/env python3
"""
Article Generator
Generates beginner-friendly AI paper explanations using OpenAI API.
"""

import openai
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import re

class ArticleGenerator:
    def __init__(self):
        # OpenAI API is already configured via environment variables
        self.client = openai.OpenAI()
        
        # Article template structure
        self.template = {
            "title": "",
            "subtitle": "",
            "category": "",
            "authors": [],
            "paper_url": "",
            "read_time": "",
            "publish_date": "",
            "concept_explained": "",
            "content": {
                "background": "",
                "methodology": "",
                "results": "",
                "significance": ""
            },
            "concept_explanation": {
                "title": "",
                "content": ""
            },
            "summary": ""
        }
    
    def generate_article(self, paper: Dict) -> Dict:
        """
        Generate a complete article from a paper dictionary.
        
        Args:
            paper: Paper information from arXiv fetcher
            
        Returns:
            Complete article dictionary
        """
        print(f"Generating article for: {paper['title']}")
        
        # Generate main content sections
        background = self._generate_background(paper)
        methodology = self._generate_methodology(paper)
        results = self._generate_results(paper)
        significance = self._generate_significance(paper)
        
        # Generate concept explanation
        concept_title, concept_content = self._generate_concept_explanation(paper)
        
        # Generate summary
        summary = self._generate_summary(paper)
        
        # Estimate read time (average 200 words per minute)
        total_words = len((background + methodology + results + significance + concept_content).split())
        read_time = max(1, round(total_words / 200))
        
        # Create article structure
        article = self.template.copy()
        article.update({
            "title": f"Paper Explained: {paper['title']} - A Beginner's Guide",
            "subtitle": self._generate_subtitle(paper),
            "category": self._format_category(paper['category']),
            "authors": paper['authors'],
            "paper_url": f"https://arxiv.org/abs/{paper['id']}",
            "read_time": f"{read_time} min read",
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
            "concept_explained": concept_title,
            "content": {
                "background": background,
                "methodology": methodology,
                "results": results,
                "significance": significance
            },
            "concept_explanation": {
                "title": f"Understanding {concept_title}: The Heart of {paper['title'].split(':')[0] if ':' in paper['title'] else paper['title']}",
                "content": concept_content
            },
            "summary": summary
        })
        
        return article
    
    def _generate_background(self, paper: Dict) -> str:
        """Generate the background section explaining why the research was needed."""
        prompt = f"""
        Write a beginner-friendly explanation of why the research in this paper was needed. 
        
        Paper Title: {paper['title']}
        Abstract: {paper['summary']}
        
        Requirements:
        - Explain in simple terms what problems existed before this research
        - Use analogies and everyday examples where possible
        - Avoid technical jargon
        - Write 2-3 paragraphs
        - Target audience: university students new to AI
        
        Focus on the motivation and context, not the solution.
        """
        
        return self._call_openai(prompt)
    
    def _generate_methodology(self, paper: Dict) -> str:
        """Generate the methodology section explaining how the research works."""
        prompt = f"""
        Explain the key innovation and methodology of this research paper in beginner-friendly terms.
        
        Paper Title: {paper['title']}
        Abstract: {paper['summary']}
        
        Requirements:
        - Break down the main approach into simple steps
        - Use analogies and metaphors to explain complex concepts
        - Avoid mathematical formulas and technical details
        - Write 3-4 paragraphs
        - Use numbered lists or bullet points where helpful
        - Target audience: university students new to AI
        
        Focus on WHAT they did and HOW it works conceptually, not the technical implementation.
        """
        
        return self._call_openai(prompt)
    
    def _generate_results(self, paper: Dict) -> str:
        """Generate the results section explaining the impact and achievements."""
        prompt = f"""
        Explain the results and achievements of this research paper in beginner-friendly terms.
        
        Paper Title: {paper['title']}
        Abstract: {paper['summary']}
        
        Requirements:
        - Explain what the research achieved
        - Compare to previous methods if relevant
        - Mention specific improvements or breakthroughs
        - Write 2-3 paragraphs
        - Use simple language and avoid technical metrics
        - Target audience: university students new to AI
        
        Focus on the practical impact and what made this work significant.
        """
        
        return self._call_openai(prompt)
    
    def _generate_significance(self, paper: Dict) -> str:
        """Generate the significance section explaining long-term impact."""
        prompt = f"""
        Explain why this research paper matters today and its long-term significance in AI.
        
        Paper Title: {paper['title']}
        Abstract: {paper['summary']}
        Published: {paper['published']}
        
        Requirements:
        - Explain how this research influenced later developments
        - Mention specific applications or systems that use this work
        - Connect to modern AI systems people know (ChatGPT, etc.)
        - Write 2-3 paragraphs
        - Use simple language
        - Target audience: university students new to AI
        
        Focus on the lasting impact and why someone should care about this paper today.
        """
        
        return self._call_openai(prompt)
    
    def _generate_concept_explanation(self, paper: Dict) -> tuple[str, str]:
        """Generate a detailed explanation of one key concept from the paper."""
        # First, identify the key concept
        concept_prompt = f"""
        Identify the single most important technical concept introduced or used in this paper that a beginner should understand.
        
        Paper Title: {paper['title']}
        Abstract: {paper['summary']}
        
        Return only the name of the concept (2-4 words maximum). Examples:
        - "Self-Attention Mechanism"
        - "Convolutional Neural Networks"
        - "Adversarial Training"
        - "Bidirectional Context"
        """
        
        concept_title = self._call_openai(concept_prompt).strip()
        
        # Then explain the concept in detail
        explanation_prompt = f"""
        Provide a detailed, beginner-friendly explanation of "{concept_title}" as it relates to the paper "{paper['title']}".
        
        Paper Abstract: {paper['summary']}
        
        Requirements:
        - Start with a simple analogy or real-world example
        - Explain how it works step by step
        - Use concrete examples
        - Explain why this concept is important
        - Write 4-5 paragraphs
        - Use simple language and avoid jargon
        - Target audience: university students new to AI
        - Include practical applications where relevant
        
        Make this explanation comprehensive enough that a beginner could understand and explain the concept to someone else.
        """
        
        concept_content = self._call_openai(explanation_prompt)
        
        return concept_title, concept_content
    
    def _generate_summary(self, paper: Dict) -> str:
        """Generate a one-sentence summary of the paper."""
        prompt = f"""
        Write a single, clear sentence that summarizes the main contribution of this research paper.
        
        Paper Title: {paper['title']}
        Abstract: {paper['summary']}
        
        Requirements:
        - One sentence only
        - Simple language
        - Capture the essence of what this paper achieved
        - Target audience: university students new to AI
        
        Example format: "This paper introduced [innovation] which [impact], becoming the foundation for [applications]."
        """
        
        return self._call_openai(prompt).strip()
    
    def _generate_subtitle(self, paper: Dict) -> str:
        """Generate an engaging subtitle for the article."""
        prompt = f"""
        Create an engaging subtitle for a beginner-friendly explanation of this research paper.
        
        Paper Title: {paper['title']}
        Abstract: {paper['summary']}
        
        Requirements:
        - 5-10 words
        - Capture the main innovation or impact
        - Make it appealing to beginners
        - Avoid technical jargon
        
        Examples:
        - "How the Transformer Architecture Revolutionized AI"
        - "The Deep Learning Breakthrough That Started It All"
        - "Two Neural Networks Competing to Create Reality"
        """
        
        return self._call_openai(prompt).strip()
    
    def _format_category(self, category_slug: str) -> str:
        """Convert category slug to display name."""
        category_map = {
            'foundation-models': 'Foundation Models',
            'generative-models': 'Generative Models',
            'optimization': 'Optimization',
            'applications': 'Applications',
            'basic-concepts': 'Basic Concepts'
        }
        return category_map.get(category_slug, 'Basic Concepts')
    
    def _call_openai(self, prompt: str) -> str:
        """Make a call to OpenAI API with error handling."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-5-nano",
                messages=[
                    {"role": "system", "content": "You are an expert at explaining complex AI research papers in simple, beginner-friendly terms. You use analogies, examples, and clear language to make technical concepts accessible to university students new to AI."},
                    {"role": "user", "content": prompt}
                ],
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return f"Error generating content: {e}"
    
    def save_article(self, article: Dict, filename: str):
        """Save article to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        print(f"Saved article to {filename}")
    
    def generate_multiple_articles(self, papers: List[Dict], output_dir: str = "articles"):
        """Generate articles for multiple papers."""
        os.makedirs(output_dir, exist_ok=True)
        
        articles = []
        for i, paper in enumerate(papers):
            try:
                article = self.generate_article(paper)
                
                # Create filename from paper ID
                filename = f"{output_dir}/article_{paper['id'].replace('/', '_')}.json"
                self.save_article(article, filename)
                
                articles.append(article)
                
                print(f"Generated article {i+1}/{len(papers)}")
                
            except Exception as e:
                print(f"Error generating article for {paper['title']}: {e}")
                continue
        
        return articles

def main():
    """Example usage of ArticleGenerator."""
    generator = ArticleGenerator()
    
    # Load papers from JSON file (created by arxiv_fetcher.py)
    try:
        with open('classic_papers.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        # Generate article for the first paper (Attention Is All You Need)
        if papers:
            article = generator.generate_article(papers[0])
            generator.save_article(article, 'sample_article.json')
            print("Sample article generated successfully!")
        
    except FileNotFoundError:
        print("Please run arxiv_fetcher.py first to generate classic_papers.json")

if __name__ == "__main__":
    main()

