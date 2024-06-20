import React from 'react';
import { ArticleType } from '../types/ArticleType';
import ArticleItem from './ArticleItem';

interface ArticleListProps {
  articles: ArticleType[];
  onArticleClick: (article: ArticleType) => void;
}

const ArticleList: React.FC<ArticleListProps> = ({ articles, onArticleClick }) => {
  //** сортировка по priority */
  const sortedArticles = [...articles].sort((a, b) => a.priority - b.priority);

  return (
    <div className='article_list'>
      (/** вывод новостей через перебор */)
      {sortedArticles.map((article) => (
        <ArticleItem key={article.url} article={article} onClick={onArticleClick} />
      ))}
    </div>
  );
};

export default ArticleList;