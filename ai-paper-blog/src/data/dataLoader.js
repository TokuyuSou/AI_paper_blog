import articlesData from './articles.json';

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
