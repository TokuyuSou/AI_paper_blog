import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import HomePage from './components/HomePage'
import ArticlePage from './components/ArticlePage'
import CategoryPage from './components/CategoryPage'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/article/:id" element={<ArticlePage />} />
            <Route path="/category/:category" element={<CategoryPage />} />
          </Routes>
        </main>
        <footer className="bg-muted py-8 mt-16">
          <div className="container mx-auto px-4 text-center text-muted-foreground">
            <p>&copy; 2025 AI Papers Explained. Making research accessible to everyone.</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App

