export interface SourceType {
  id: string | null;
  name: string;
}

export interface ArticleType {
  priority: number;
  source: SourceType;
  author: string;
  title: string;
  description: string;
  url: string;
  urlToImage: string;
  publishedAt: string;
  content: string;
}