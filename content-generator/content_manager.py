#!/usr/bin/env python3
"""
Content Manager
Manages the integration of generated articles into the React blog.
"""

import json
import os
import shutil
from typing import Dict, List
from datetime import datetime
import re

class ContentManager:
    def __init__(self, blog_path: str = "/home/ubuntu/ai-paper-blog"):
        self.blog_path = blog_path
        self.articles_dir = os.path.join(blog_path, "src", "data")
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure necessary directories exist."""
        os.makedirs(self.articles_dir, exist_ok=True)
    
    def integrate_articles(self, articles: List[Dict]):
        """
        Integrate generated articles into the React blog.
        
        Args:
            articles: List of article dictionaries from ArticleGenerator
        """
        print(f"Integrating {len(articles)} articles into the blog...")
        
        # Create articles data file
        articles_data = []
        
        for article in articles:
            # Create article data structure for React
            article_data = {
                "id": self._create_article_id(article["title"]),
                "title": article["title"],
                "subtitle": article["subtitle"],
                "category": article["category"],
                "categorySlug": self._get_category_slug(article["category"]),
                "authors": article["authors"],
                "paperUrl": article["paper_url"],
                "readTime": article["read_time"],
                "publishDate": article["publish_date"],
                "conceptExplained": article["concept_explained"],
                "content": article["content"],
                "conceptExplanation": article["concept_explanation"],
                "summary": article["summary"],
                "excerpt": self._create_excerpt(article["content"]["background"])
            }
            
            articles_data.append(article_data)
        
        # Save articles data
        articles_file = os.path.join(self.articles_dir, "articles.json")
        with open(articles_file, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, indent=2, ensure_ascii=False)
        
        print(f"Articles data saved to {articles_file}")
        
        # Update React components to use the data
        self._update_react_components()
        
        return articles_data
    
    def _create_article_id(self, title: str) -> str:
        """Create a URL-friendly article ID from title."""
        # Extract the paper title part (after "Paper Explained: ")
        if "Paper Explained: " in title:
            paper_title = title.split("Paper Explained: ")[1]
            if " - " in paper_title:
                paper_title = paper_title.split(" - ")[0]
        else:
            paper_title = title
        
        # Convert to slug
        slug = re.sub(r'[^\w\s-]', '', paper_title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def _get_category_slug(self, category: str) -> str:
        """Convert category display name to slug."""
        category_map = {
            'Foundation Models': 'foundation-models',
            'Generative Models': 'generative-models',
            'Optimization': 'optimization',
            'Applications': 'applications',
            'Basic Concepts': 'basic-concepts'
        }
        return category_map.get(category, 'basic-concepts')
    
    def _create_excerpt(self, background: str) -> str:
        """Create a short excerpt from the background section."""
        sentences = background.split('. ')
        if len(sentences) >= 2:
            return '. '.join(sentences[:2]) + '.'
        return background[:200] + '...' if len(background) > 200 else background
    
    def _update_react_components(self):
        """Update React components to use dynamic data instead of hardcoded content."""
        
        # Create data loader utility
        data_loader_content = '''import articlesData from './articles.json';

export const getArticles = () => {
  return articlesData;
};

export const getArticleById = (id) => {
  return articlesData.find(article => article.id === id);
};

export const getArticlesByCategory = (categorySlug) => {
  return articlesData.filter(article => article.categorySlug === categorySlug);
};

export const getFeaturedArticles = (limit = 3) => {
  return articlesData.slice(0, limit);
};

export const getCategories = () => {
  const categories = {};
  articlesData.forEach(article => {
    if (!categories[article.categorySlug]) {
      categories[article.categorySlug] = {
        name: article.category,
        slug: article.categorySlug,
        count: 0
      };
    }
    categories[article.categorySlug].count++;
  });
  return Object.values(categories);
};
'''
        
        data_loader_path = os.path.join(self.articles_dir, "dataLoader.js")
        with open(data_loader_path, 'w', encoding='utf-8') as f:
            f.write(data_loader_content)
        
        print(f"Data loader created at {data_loader_path}")
        
        # Update HomePage component
        self._update_homepage_component()
        
        # Update ArticlePage component
        self._update_article_page_component()
        
        # Update CategoryPage component
        self._update_category_page_component()
    
    def _update_homepage_component(self):
        """Update HomePage component to use dynamic data."""
        homepage_content = '''import { Link } from 'react-router-dom'
import { Calendar, Clock, ArrowRight, BookOpen, Users, Target } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { getFeaturedArticles, getCategories } from '../data/dataLoader'

const HomePage = () => {
  const featuredArticles = getFeaturedArticles(3);
  const categories = getCategories();
  const totalArticles = featuredArticles.length;

  const stats = [
    { icon: BookOpen, label: 'Papers Explained', value: `${totalArticles}+` },
    { icon: Users, label: 'Monthly Readers', value: '10K+' },
    { icon: Target, label: 'Concepts Covered', value: `${totalArticles * 5}+` }
  ]

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <h1 className="text-4xl md:text-6xl font-bold text-foreground">
          AI Research Made
          <span className="text-primary"> Simple</span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
          Complex AI papers explained in plain English. Perfect for students, researchers, and anyone curious about the latest breakthroughs in artificial intelligence.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" asChild>
            <Link to="/category/foundation-models">
              Start Reading <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
          <Button variant="outline" size="lg" asChild>
            <a href="#about">Learn More</a>
          </Button>
        </div>
      </section>

      {/* Stats Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {stats.map((stat, index) => (
          <div key={index} className="text-center space-y-2">
            <stat.icon className="h-8 w-8 mx-auto text-primary" />
            <div className="text-3xl font-bold text-foreground">{stat.value}</div>
            <div className="text-muted-foreground">{stat.label}</div>
          </div>
        ))}
      </section>

      {/* Featured Articles */}
      <section className="space-y-8">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold text-foreground">Latest Explanations</h2>
          <p className="text-muted-foreground">
            Dive into the most influential AI papers, explained for beginners
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredArticles.map((article) => (
            <Card key={article.id} className="group hover:shadow-lg transition-shadow duration-300">
              <div className="aspect-video bg-muted rounded-t-lg overflow-hidden">
                <div className="w-full h-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center">
                  <BookOpen className="h-12 w-12 text-primary/60" />
                </div>
              </div>
              <CardHeader className="space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="secondary">{article.category}</Badge>
                  <div className="flex items-center text-sm text-muted-foreground">
                    <Clock className="h-4 w-4 mr-1" />
                    {article.readTime}
                  </div>
                </div>
                <CardTitle className="group-hover:text-primary transition-colors">
                  <Link to={`/article/${article.id}`}>
                    {article.title}
                  </Link>
                </CardTitle>
                <CardDescription>{article.excerpt}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4 mr-2" />
                  {new Date(article.publishDate).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <div className="text-sm font-medium text-foreground">Concept Explained:</div>
                  <div className="text-sm text-muted-foreground">{article.conceptExplained}</div>
                </div>
                <Button variant="ghost" className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors" asChild>
                  <Link to={`/article/${article.id}`}>
                    Read Full Explanation <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="bg-muted rounded-lg p-8 md:p-12 space-y-6">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold text-foreground">Why AI Papers Explained?</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            We believe that groundbreaking AI research should be accessible to everyone, not just experts with PhDs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-foreground">🎯 For Beginners</h3>
            <p className="text-muted-foreground">
              Every paper is explained using simple language, analogies, and visual concepts that anyone can understand.
            </p>
          </div>
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-foreground">📚 Concept Dictionary</h3>
            <p className="text-muted-foreground">
              Each article includes detailed explanations of key concepts, building your AI vocabulary over time.
            </p>
          </div>
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-foreground">🔄 Regular Updates</h3>
            <p className="text-muted-foreground">
              From classic papers to the latest research, we cover both foundational knowledge and cutting-edge developments.
            </p>
          </div>
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-foreground">🎓 Learning Path</h3>
            <p className="text-muted-foreground">
              Start with fundamentals and gradually work your way up to understanding the most advanced AI research.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage'''
        
        homepage_path = os.path.join(self.blog_path, "src", "components", "HomePage.jsx")
        with open(homepage_path, 'w', encoding='utf-8') as f:
            f.write(homepage_content)
        
        print("Updated HomePage component to use dynamic data")
    
    def _update_article_page_component(self):
        """Update ArticlePage component to use dynamic data."""
        article_page_content = '''import { useParams, Link } from 'react-router-dom'
import { Calendar, Clock, ArrowLeft, BookOpen, Lightbulb, Target, TrendingUp } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { getArticleById } from '../data/dataLoader'

const ArticlePage = () => {
  const { id } = useParams()
  const article = getArticleById(id)

  if (!article) {
    return (
      <div className="max-w-4xl mx-auto text-center py-16">
        <h1 className="text-2xl font-bold text-foreground mb-4">Article Not Found</h1>
        <p className="text-muted-foreground mb-8">The article you're looking for doesn't exist.</p>
        <Button asChild>
          <Link to="/">Back to Home</Link>
        </Button>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Back Button */}
      <Button variant="ghost" asChild>
        <Link to="/">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Articles
        </Link>
      </Button>

      {/* Article Header */}
      <div className="space-y-6">
        <div className="space-y-4">
          <Badge variant="secondary">{article.category}</Badge>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground leading-tight">
            {article.title}
          </h1>
          <p className="text-xl text-muted-foreground">{article.subtitle}</p>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center">
            <Calendar className="h-4 w-4 mr-2" />
            {new Date(article.publishDate).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </div>
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-2" />
            {article.readTime}
          </div>
          <Button variant="outline" size="sm" asChild>
            <a href={article.paperUrl} target="_blank" rel="noopener noreferrer">
              <BookOpen className="h-4 w-4 mr-2" />
              Read Original Paper
            </a>
          </Button>
        </div>

        <div className="text-sm text-muted-foreground">
          <strong>Authors:</strong> {article.authors.join(', ')}
        </div>
      </div>

      <Separator />

      {/* Article Content */}
      <div className="prose prose-lg max-w-none space-y-8">
        {/* Background Section */}
        <section className="space-y-4">
          <div className="flex items-center space-x-2">
            <Target className="h-6 w-6 text-primary" />
            <h2 className="text-2xl font-bold text-foreground">Background: Why This Research Was Needed</h2>
          </div>
          <div className="text-muted-foreground leading-relaxed">
            {article.content.background.split('\\n\\n').map((paragraph, index) => (
              <p key={index} className="mb-4">{paragraph}</p>
            ))}
          </div>
        </section>

        <Separator />

        {/* Methodology Section */}
        <section className="space-y-4">
          <div className="flex items-center space-x-2">
            <Lightbulb className="h-6 w-6 text-primary" />
            <h2 className="text-2xl font-bold text-foreground">The Key Innovation: How It Works</h2>
          </div>
          <div className="text-muted-foreground leading-relaxed">
            {article.content.methodology.split('\\n\\n').map((paragraph, index) => (
              <p key={index} className="mb-4">{paragraph}</p>
            ))}
          </div>
        </section>

        <Separator />

        {/* Results Section */}
        <section className="space-y-4">
          <div className="flex items-center space-x-2">
            <TrendingUp className="h-6 w-6 text-primary" />
            <h2 className="text-2xl font-bold text-foreground">Results and Impact</h2>
          </div>
          <div className="text-muted-foreground leading-relaxed">
            {article.content.results.split('\\n\\n').map((paragraph, index) => (
              <p key={index} className="mb-4">{paragraph}</p>
            ))}
          </div>
        </section>

        <Separator />

        {/* Significance Section */}
        <section className="space-y-4">
          <div className="flex items-center space-x-2">
            <BookOpen className="h-6 w-6 text-primary" />
            <h2 className="text-2xl font-bold text-foreground">Why This Matters Today</h2>
          </div>
          <div className="text-muted-foreground leading-relaxed">
            {article.content.significance.split('\\n\\n').map((paragraph, index) => (
              <p key={index} className="mb-4">{paragraph}</p>
            ))}
          </div>
        </section>
      </div>

      <Separator />

      {/* Concept Explanation */}
      <Card className="bg-primary/5 border-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Lightbulb className="h-5 w-5 text-primary" />
            <span>Concept Deep Dive</span>
          </CardTitle>
          <CardDescription>{article.conceptExplanation.title}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="text-muted-foreground leading-relaxed">
            {article.conceptExplanation.content.split('\\n\\n').map((paragraph, index) => (
              <p key={index} className="mb-4">{paragraph}</p>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Summary */}
      <Card>
        <CardHeader>
          <CardTitle>One-Sentence Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg text-muted-foreground">
            {article.summary}
          </p>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between items-center pt-8">
        <Button variant="outline" asChild>
          <Link to="/">
            <ArrowLeft className="mr-2 h-4 w-4" />
            More Articles
          </Link>
        </Button>
        <Button asChild>
          <Link to={`/category/${article.categorySlug}`}>
            Explore {article.category}
          </Link>
        </Button>
      </div>
    </div>
  )
}

export default ArticlePage'''
        
        article_page_path = os.path.join(self.blog_path, "src", "components", "ArticlePage.jsx")
        with open(article_page_path, 'w', encoding='utf-8') as f:
            f.write(article_page_content)
        
        print("Updated ArticlePage component to use dynamic data")
    
    def _update_category_page_component(self):
        """Update CategoryPage component to use dynamic data."""
        category_page_content = '''import { useParams, Link } from 'react-router-dom'
import { Calendar, Clock, ArrowLeft, BookOpen, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { getArticlesByCategory, getCategories } from '../data/dataLoader'

const CategoryPage = () => {
  const { category } = useParams()
  const articles = getArticlesByCategory(category)
  const categories = getCategories()

  // Category information
  const categoryInfo = {
    'foundation-models': {
      name: 'Foundation Models & LLMs',
      description: 'Explore the architectures that power modern AI systems, from Transformers to GPT and BERT.',
      icon: '🏗️'
    },
    'generative-models': {
      name: 'Generative Models',
      description: 'Understand how AI creates new content, from GANs to Diffusion Models and VAEs.',
      icon: '🎨'
    },
    'optimization': {
      name: 'Optimization & Efficiency',
      description: 'Learn about techniques that make AI models faster, smaller, and more efficient.',
      icon: '⚡'
    },
    'applications': {
      name: 'AI Applications',
      description: 'Discover how AI is being applied in healthcare, robotics, education, and beyond.',
      icon: '🚀'
    },
    'basic-concepts': {
      name: 'Basic Concepts',
      description: 'Master the fundamental building blocks of artificial intelligence and machine learning.',
      icon: '📚'
    }
  }

  const currentCategory = categoryInfo[category] || {
    name: 'Category Not Found',
    description: 'This category does not exist.',
    icon: '❓'
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Back Button */}
      <Button variant="ghost" asChild>
        <Link to="/">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Home
        </Link>
      </Button>

      {/* Category Header */}
      <div className="text-center space-y-6 py-8">
        <div className="text-6xl">{currentCategory.icon}</div>
        <h1 className="text-3xl md:text-4xl font-bold text-foreground">
          {currentCategory.name}
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          {currentCategory.description}
        </p>
        <Badge variant="secondary" className="text-sm">
          {articles.length} Articles Available
        </Badge>
      </div>

      {/* Articles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {articles.map((article) => (
          <Card key={article.id} className="group hover:shadow-lg transition-shadow duration-300">
            <div className="aspect-video bg-muted rounded-t-lg overflow-hidden">
              <div className="w-full h-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center">
                <BookOpen className="h-12 w-12 text-primary/60" />
              </div>
            </div>
            <CardHeader className="space-y-3">
              <div className="flex items-center justify-between">
                <Badge variant="outline">{article.category}</Badge>
                <div className="flex items-center text-sm text-muted-foreground">
                  <Clock className="h-4 w-4 mr-1" />
                  {article.readTime}
                </div>
              </div>
              <CardTitle className="group-hover:text-primary transition-colors">
                <Link to={`/article/${article.id}`}>
                  {article.title}
                </Link>
              </CardTitle>
              <CardDescription>{article.excerpt}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center text-sm text-muted-foreground">
                <Calendar className="h-4 w-4 mr-2" />
                {new Date(article.publishDate).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </div>
              <div className="p-3 bg-muted rounded-lg">
                <div className="text-sm font-medium text-foreground">Concept Explained:</div>
                <div className="text-sm text-muted-foreground">{article.conceptExplained}</div>
              </div>
              <Button 
                variant="ghost" 
                className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors" 
                asChild
              >
                <Link to={`/article/${article.id}`}>
                  Read Full Explanation <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {articles.length === 0 && (
        <div className="text-center py-12 space-y-4">
          <BookOpen className="h-16 w-16 mx-auto text-muted-foreground" />
          <h3 className="text-xl font-semibold text-foreground">No Articles Yet</h3>
          <p className="text-muted-foreground">
            We're working on adding more articles to this category. Check back soon!
          </p>
          <Button asChild>
            <Link to="/">Browse Other Categories</Link>
          </Button>
        </div>
      )}

      {/* Related Categories */}
      <div className="bg-muted rounded-lg p-8 space-y-6">
        <h2 className="text-2xl font-bold text-foreground text-center">Explore Other Categories</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(categoryInfo)
            .filter(([slug]) => slug !== category)
            .map(([slug, info]) => (
              <Link
                key={slug}
                to={`/category/${slug}`}
                className="text-center p-4 rounded-lg hover:bg-background transition-colors group"
              >
                <div className="text-3xl mb-2">{info.icon}</div>
                <div className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">
                  {info.name}
                </div>
              </Link>
            ))}
        </div>
      </div>
    </div>
  )
}

export default CategoryPage'''
        
        category_page_path = os.path.join(self.blog_path, "src", "components", "CategoryPage.jsx")
        with open(category_page_path, 'w', encoding='utf-8') as f:
            f.write(category_page_content)
        
        print("Updated CategoryPage component to use dynamic data")

def main():
    """Example usage of ContentManager."""
    manager = ContentManager()
    
    # Load generated articles
    try:
        articles = []
        articles_dir = "articles"
        if os.path.exists(articles_dir):
            for filename in os.listdir(articles_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(articles_dir, filename), 'r', encoding='utf-8') as f:
                        article = json.load(f)
                        articles.append(article)
        
        if articles:
            manager.integrate_articles(articles)
            print(f"Successfully integrated {len(articles)} articles into the blog!")
        else:
            print("No articles found. Please generate articles first.")
            
    except Exception as e:
        print(f"Error integrating articles: {e}")

if __name__ == "__main__":
    main()

