import React, { useEffect, useState } from "react";
import ArticleList from "./components/ArticleList";
import ArticleModal from "./components/ArticleModal";
import { ArticleType } from "./types/ArticleType";
import "./App.css";

//** Пример ответа от сервера */
const initialArticles: ArticleType[] = [
  {
    priority: 1,
    source: { id: '1', name: 'Source Name' },
    author: 'Author Name',
    title: 'Article Title',
    description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!',
    url: 'https://example.com',
    urlToImage: 'https://example.com/image.jpg',
    publishedAt: '2024-06-20T12:00:00Z',
    content: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam! Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!'
  },
  {
    priority: 2,
    source: { id: '2', name: 'Source Name 2' },
    author: 'Author Name 2',
    title: 'Article Title 2',
    description: 'Article Description 2 Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam! Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam! Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!',
    url: 'https://example.com',
    urlToImage: 'https://example.com/image.jpg',
    publishedAt: '2024-06-20T12:00:00Z',
    content: 'Article content 2 goes here. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!'
  },
  {
    priority: 3,
    source: { id: '3', name: 'Source Name 3' },
    author: 'Author Name 3',
    title: 'Article Title 3',
    description: 'Article Description 3 Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!',
    url: 'https://example.com',
    urlToImage: 'https://example.com/image.jpg',
    publishedAt: '2024-06-20T12:00:00Z',
    content: 'Article content 3 goes here. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!'
  },
  {
    priority: 4,
    source: { id: '4', name: 'Source Name 4' },
    author: 'Author Name 4',
    title: 'Article Title 4',
    description: 'Article Description 4 Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!',
    url: 'https://example.com',
    urlToImage: 'https://example.com/image.jpg',
    publishedAt: '2024-06-20T12:00:00Z',
    content: 'Article content 4 goes here. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!'
  },
  {
    priority: 5,
    source: { id: '5', name: 'Source Name 5' },
    author: 'Author Name 5',
    title: 'Article Title 5',
    description: 'Article Description 5 Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!',
    url: 'https://example.com',
    urlToImage: 'https://example.com/image.jpg',
    publishedAt: '2024-06-20T12:00:00Z',
    content: 'Article content 5 goes here. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Unde rerum aliquam illo facere numquam? Iure, quae, aliquid tempora cumque ducimus quisquam harum consequuntur vero numquam sit optio rerum deleniti aliquam!'
  },
];

const App: React.FC = () => {
  const [articles, setArticles] = useState<ArticleType[]>(initialArticles);
  const [selectedArticle, setSelectedArticle] = useState<ArticleType | null>(null);

   //** Подключение вебсокета */
  useEffect(() => {
    const wbSocket = new WebSocket("ws://your-websocket-server-url");

    wbSocket.onopen = () => {
      console.log("Connected to WebSocket");
    };

    wbSocket.onmessage = (event) => {
      //** Подписка на получение сообщений из сервера */
      const message = JSON.parse(event.data);
      if (message.articlesAdd) {
        setArticles((prevArticles) => [
          ...prevArticles,
          ...message.articlesAdd,
        ]);
      }
      if (message.articlesUpdate) {
        setArticles((prevArticles) =>
          prevArticles.map(
            (article) =>
              message.articlesUpdate.find(
                (updatedArticle: ArticleType) => updatedArticle.url === article.url
              ) || article
          )
        );
      }
    };

    return () => {
      wbSocket.close();
    };
  }, []);


  const handleArticleClick = (article: ArticleType) => {
    setSelectedArticle(article);
  };

  const handleCloseModal = () => {
    setSelectedArticle(null);
  };

  return (
    <section className="App">
      <h1 className="title">Advanced Media</h1>
      <div className="articles_container">
        <ArticleList articles={articles} onArticleClick={handleArticleClick}/> 
        <ArticleModal article={selectedArticle} onClose={handleCloseModal} />
      </div>
    </section>
  );
};

export default App;
