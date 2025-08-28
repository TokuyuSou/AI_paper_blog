import { useParams, Link } from 'react-router-dom'
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

export default CategoryPage