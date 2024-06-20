// src/components/ArticleModal.tsx
import React from 'react';
import { ArticleType } from '../types/ArticleType';

interface ArticleModalProps {
  article: ArticleType | null;
  onClose: () => void;
}

const ArticleModal: React.FC<ArticleModalProps> = ({ article, onClose }) => {
  if (!article) return null;

  return (
    <div className='article_modal'>
      <div>
        <h2>{article.title}</h2>
        <p>by {article.author}</p>
        <p>{article.description}</p>
        <img src={article.urlToImage} alt={article.title} style={{ width: '100%' }} />
        <p>{article.content}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default ArticleModal;
