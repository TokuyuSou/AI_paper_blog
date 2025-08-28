import { useParams, Link } from 'react-router-dom'
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
            {article.content.background.split('\n\n').map((paragraph, index) => (
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
            {article.content.methodology.split('\n\n').map((paragraph, index) => (
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
            {article.content.results.split('\n\n').map((paragraph, index) => (
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
            {article.content.significance.split('\n\n').map((paragraph, index) => (
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
            {article.conceptExplanation.content.split('\n\n').map((paragraph, index) => (
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

export default ArticlePage