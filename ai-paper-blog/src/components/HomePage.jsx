import { Link } from 'react-router-dom'
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

export default HomePage