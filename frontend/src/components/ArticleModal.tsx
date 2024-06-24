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
    <div className='article_modal_container'>
      <div className='article_modal'>
        <h2>{article.title}</h2>
        <p>by {article.author}</p>
        <p>{article.description}</p>
        <img src={article.urlToImage} alt="article images" style={{ width: '100%' }} />
        <p>{article.content}</p>
        <button onClick={onClose}>
          Close
          <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24">
            <path fill="none" stroke="#fff" strokeLinecap="round" strokeLinejoin="round" d="m7 7l10 10M7 17L17 7"></path>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default ArticleModal;
