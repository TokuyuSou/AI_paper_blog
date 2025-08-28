#!/usr/bin/env python3
"""
Daily Automation Script
Automatically generates new AI/ML paper articles and integrates them into the blog.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from enhanced_arxiv_fetcher import EnhancedArxivFetcher
from article_generator import ArticleGenerator
from content_manager import ContentManager

class DailyAutomation:
    def __init__(self):
        self.fetcher = EnhancedArxivFetcher()
        self.generator = ArticleGenerator()
        self.content_manager = ContentManager()
        self.max_daily_articles = 2  # Limit to 2 new articles per day
        
    def load_existing_articles(self):
        """Load existing articles to avoid duplicates."""
        try:
            articles_file = os.path.join('..', 'ai-paper-blog', 'src', 'data', 'articles.json')
            if os.path.exists(articles_file):
                with open(articles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading existing articles: {e}")
            return []
    
    def get_existing_paper_ids(self, articles):
        """Extract paper IDs from existing articles."""
        existing_ids = set()
        for article in articles:
            # Extract arXiv ID from URL or paper_id field
            if 'paper_id' in article:
                existing_ids.add(article['paper_id'])
            elif 'url' in article and 'arxiv.org/abs/' in article['url']:
                paper_id = article['url'].split('/')[-1]
                existing_ids.add(paper_id)
        return existing_ids
    
    def find_new_papers(self):
        """Find new papers that haven't been covered yet."""
        print("Searching for new papers...")
        
        # Load existing articles
        existing_articles = self.load_existing_articles()
        existing_ids = self.get_existing_paper_ids(existing_articles)
        
        print(f"Found {len(existing_ids)} existing articles")
        
        # Search for recent papers
        recent_papers = self.fetcher.search_recent_papers(
            query="transformer OR attention OR neural network OR deep learning",
            max_results=20,
            days_back=7
        )
        
        # Filter out papers we already have
        new_papers = []
        for paper in recent_papers:
            if paper['id'] not in existing_ids:
                new_papers.append(paper)
        
        print(f"Found {len(new_papers)} new papers")
        
        # Sort by relevance score and return top papers
        new_papers.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return new_papers[:self.max_daily_articles]
    
    def generate_articles_for_papers(self, papers):
        """Generate articles for the given papers."""
        generated_articles = []
        
        for paper in papers:
            try:
                print(f"Generating article for: {paper['title']}")
                
                # Generate article
                article_data = self.generator.generate_article(paper)
                
                if article_data:
                    # Add paper metadata
                    article_data['paper_id'] = paper['id']
                    article_data['arxiv_url'] = f"https://arxiv.org/abs/{paper['id']}"
                    article_data['categories'] = paper.get('categories', [])
                    
                    generated_articles.append(article_data)
                    print(f"Successfully generated article for {paper['id']}")
                else:
                    print(f"Failed to generate article for {paper['id']}")
                    
            except Exception as e:
                print(f"Error generating article for {paper['id']}: {e}")
                continue
        
        return generated_articles
    
    def save_generated_articles(self, articles):
        """Save generated articles to individual JSON files."""
        os.makedirs('generated_content/articles', exist_ok=True)
        
        for article in articles:
            filename = f"generated_content/articles/daily_{article['paper_id']}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(article, f, indent=2, ensure_ascii=False)
            print(f"Saved article to {filename}")
    
    def integrate_articles(self, articles):
        """Integrate new articles into the blog."""
        if not articles:
            print("No new articles to integrate")
            return
        
        try:
            # Use content manager to integrate articles
            self.content_manager.integrate_articles_to_blog(articles)
            print(f"Successfully integrated {len(articles)} new articles into blog")
        except Exception as e:
            print(f"Error integrating articles: {e}")
    
    def run_daily_update(self):
        """Run the daily update process."""
        print(f"Starting daily update at {datetime.now()}")
        
        try:
            # Find new papers
            new_papers = self.find_new_papers()
            
            if not new_papers:
                print("No new papers found. Exiting.")
                return
            
            print(f"Processing {len(new_papers)} new papers:")
            for paper in new_papers:
                print(f"  - {paper['title']} (Score: {paper.get('relevance_score', 0)})")
            
            # Generate articles
            articles = self.generate_articles_for_papers(new_papers)
            
            if not articles:
                print("No articles were generated successfully. Exiting.")
                return
            
            # Save articles
            self.save_generated_articles(articles)
            
            # Integrate into blog
            self.integrate_articles(articles)
            
            print(f"Daily update completed successfully. Generated {len(articles)} new articles.")
            
        except Exception as e:
            print(f"Error during daily update: {e}")
            sys.exit(1)

def main():
    """Main function for daily automation."""
    automation = DailyAutomation()
    automation.run_daily_update()

if __name__ == "__main__":
    main()

