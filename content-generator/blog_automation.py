#!/usr/bin/env python3
"""
Blog Automation Script
Main script for automated AI paper blog content generation and management.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict

# Import our custom modules
from arxiv_fetcher import ArxivFetcher
from article_generator import ArticleGenerator
from content_manager import ContentManager

class BlogAutomation:
    def __init__(self, blog_path: str = "/home/ubuntu/ai-paper-blog"):
        self.blog_path = blog_path
        self.fetcher = ArxivFetcher()
        self.generator = ArticleGenerator()
        self.manager = ContentManager(blog_path)
        
        # Create output directories
        self.output_dir = "generated_content"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/papers", exist_ok=True)
        os.makedirs(f"{self.output_dir}/articles", exist_ok=True)
    
    def generate_classic_content(self):
        """Generate content for classic papers."""
        print("=== Generating Classic Paper Content ===")
        
        # Get classic papers
        papers = self.fetcher.get_classic_papers()
        print(f"Found {len(papers)} classic papers")
        
        # Save papers data
        papers_file = f"{self.output_dir}/papers/classic_papers.json"
        self.fetcher.save_papers_to_json(papers, papers_file)
        
        # Generate articles for classic papers
        articles = []
        for i, paper in enumerate(papers):
            print(f"\nGenerating article {i+1}/{len(papers)}: {paper['title']}")
            try:
                article = self.generator.generate_article(paper)
                articles.append(article)
                
                # Save individual article
                article_file = f"{self.output_dir}/articles/classic_{paper['id'].replace('/', '_')}.json"
                self.generator.save_article(article, article_file)
                
            except Exception as e:
                print(f"Error generating article for {paper['title']}: {e}")
                continue
        
        print(f"\nGenerated {len(articles)} articles successfully!")
        return articles
    
    def generate_recent_content(self, days: int = 7, max_papers: int = 5):
        """Generate content for recent papers."""
        print(f"=== Generating Recent Paper Content (last {days} days) ===")
        
        # Get recent papers
        papers = self.fetcher.get_recent_papers(days=days)[:max_papers]
        print(f"Found {len(papers)} recent papers")
        
        if not papers:
            print("No recent papers found")
            return []
        
        # Save papers data
        papers_file = f"{self.output_dir}/papers/recent_papers.json"
        self.fetcher.save_papers_to_json(papers, papers_file)
        
        # Generate articles for recent papers
        articles = []
        for i, paper in enumerate(papers):
            print(f"\nGenerating article {i+1}/{len(papers)}: {paper['title']}")
            try:
                article = self.generator.generate_article(paper)
                articles.append(article)
                
                # Save individual article
                article_file = f"{self.output_dir}/articles/recent_{paper['id'].replace('/', '_')}.json"
                self.generator.save_article(article, article_file)
                
            except Exception as e:
                print(f"Error generating article for {paper['title']}: {e}")
                continue
        
        print(f"\nGenerated {len(articles)} articles successfully!")
        return articles
    
    def search_and_generate(self, query: str, category: str = None, max_results: int = 3):
        """Search for papers and generate articles."""
        print(f"=== Searching and Generating Content for: {query} ===")
        
        # Search for papers
        papers = self.fetcher.search_papers(query, max_results=max_results, category=category)
        print(f"Found {len(papers)} papers")
        
        if not papers:
            print("No papers found for the query")
            return []
        
        # Save papers data
        query_safe = query.replace(' ', '_').replace('/', '_')
        papers_file = f"{self.output_dir}/papers/search_{query_safe}.json"
        self.fetcher.save_papers_to_json(papers, papers_file)
        
        # Generate articles
        articles = []
        for i, paper in enumerate(papers):
            print(f"\nGenerating article {i+1}/{len(papers)}: {paper['title']}")
            try:
                article = self.generator.generate_article(paper)
                articles.append(article)
                
                # Save individual article
                article_file = f"{self.output_dir}/articles/search_{query_safe}_{i+1}.json"
                self.generator.save_article(article, article_file)
                
            except Exception as e:
                print(f"Error generating article for {paper['title']}: {e}")
                continue
        
        print(f"\nGenerated {len(articles)} articles successfully!")
        return articles
    
    def integrate_all_content(self):
        """Integrate all generated articles into the blog."""
        print("=== Integrating Content into Blog ===")
        
        # Collect all generated articles
        articles = []
        articles_dir = f"{self.output_dir}/articles"
        
        if os.path.exists(articles_dir):
            for filename in os.listdir(articles_dir):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(articles_dir, filename), 'r', encoding='utf-8') as f:
                            article = json.load(f)
                            articles.append(article)
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
        
        if articles:
            # Sort articles by publication date (newest first)
            articles.sort(key=lambda x: x.get('publish_date', ''), reverse=True)
            
            # Integrate into blog
            self.manager.integrate_articles(articles)
            print(f"Successfully integrated {len(articles)} articles into the blog!")
            
            return articles
        else:
            print("No articles found to integrate")
            return []
    
    def full_automation(self, include_recent: bool = False):
        """Run full automation pipeline."""
        print("=== Starting Full Blog Automation ===")
        start_time = datetime.now()
        
        all_articles = []
        
        # Generate classic content
        classic_articles = self.generate_classic_content()
        all_articles.extend(classic_articles)
        
        # Generate recent content if requested
        if include_recent:
            recent_articles = self.generate_recent_content()
            all_articles.extend(recent_articles)
        
        # Integrate all content
        if all_articles:
            self.integrate_all_content()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n=== Automation Complete ===")
        print(f"Total articles generated: {len(all_articles)}")
        print(f"Duration: {duration}")
        print(f"Blog path: {self.blog_path}")
        
        return all_articles
    
    def create_sample_article(self, paper_id: str = "1706.03762"):
        """Create a single sample article for testing."""
        print(f"=== Creating Sample Article for Paper ID: {paper_id} ===")
        
        # Get the specific paper
        classic_papers = self.fetcher.get_classic_papers()
        paper = next((p for p in classic_papers if p['id'] == paper_id), None)
        
        if not paper:
            print(f"Paper with ID {paper_id} not found in classic papers")
            return None
        
        # Generate article
        try:
            article = self.generator.generate_article(paper)
            
            # Save article
            article_file = f"{self.output_dir}/articles/sample_{paper_id.replace('/', '_')}.json"
            self.generator.save_article(article, article_file)
            
            print(f"Sample article generated successfully: {article_file}")
            return article
            
        except Exception as e:
            print(f"Error generating sample article: {e}")
            return None

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="AI Paper Blog Automation")
    parser.add_argument('--mode', choices=['classic', 'recent', 'search', 'integrate', 'full', 'sample'], 
                       default='sample', help='Automation mode')
    parser.add_argument('--query', type=str, help='Search query for papers')
    parser.add_argument('--category', type=str, help='arXiv category (e.g., cs.LG, cs.CL)')
    parser.add_argument('--max-results', type=int, default=3, help='Maximum number of results')
    parser.add_argument('--days', type=int, default=7, help='Days to look back for recent papers')
    parser.add_argument('--blog-path', type=str, default='/home/ubuntu/ai-paper-blog', 
                       help='Path to the blog directory')
    parser.add_argument('--paper-id', type=str, default='1706.03762', 
                       help='Paper ID for sample generation')
    
    args = parser.parse_args()
    
    # Initialize automation
    automation = BlogAutomation(args.blog_path)
    
    try:
        if args.mode == 'classic':
            automation.generate_classic_content()
        elif args.mode == 'recent':
            automation.generate_recent_content(days=args.days, max_papers=args.max_results)
        elif args.mode == 'search':
            if not args.query:
                print("Error: --query is required for search mode")
                sys.exit(1)
            automation.search_and_generate(args.query, args.category, args.max_results)
        elif args.mode == 'integrate':
            automation.integrate_all_content()
        elif args.mode == 'full':
            automation.full_automation(include_recent=True)
        elif args.mode == 'sample':
            automation.create_sample_article(args.paper_id)
        
        print("\nAutomation completed successfully!")
        
    except KeyboardInterrupt:
        print("\nAutomation interrupted by user")
    except Exception as e:
        print(f"\nError during automation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

