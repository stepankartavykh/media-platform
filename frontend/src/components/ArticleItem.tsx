import React from 'react';
import { ArticleType } from '../types/ArticleType';

interface ArticleItemProps {
  article: ArticleType;
  onClick: (article: ArticleType) => void;
}

const ArticleItem: React.FC<ArticleItemProps> = ({ article, onClick }) => {
  return (
    <div onClick={() => onClick(article)} className='article_item'>
      <h2>{article.title}</h2>
      <p>{article.description}</p>
      <button>
        Go to 
        <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24">
          <path fill="#fff" d="M16.01 11H4v2h12.01v3L20 12l-3.99-4z"></path>
        </svg>
      </button>
    </div>
  );
};

export default ArticleItem;
