import os
from newsapi import NewsApiClient
from app.core.config import settings

def fetch_real_news_data(topic: str, output_dir: str) -> str:
    """
    Fetches real news articles on a given topic using the NewsAPI
    and saves them to a text file.
    """
    print(f"--- FETCHING REAL NEWS from NewsAPI for topic: '{topic}' ---")
    newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

    try:
        all_articles = newsapi.get_everything(
            q=topic,
            language='en',
            sort_by='relevancy',
            page_size=100  # Max articles
        )

        if not all_articles['articles']:
            raise FileNotFoundError(f"No articles found for topic: {topic}")

        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{topic.replace(' ', '_')}_real_data.txt")

        with open(file_path, 'w', encoding='utf-8') as f:
            for article in all_articles['articles']:
                content = article.get('content') or article.get('description', '')
                if content:
                    # Basic cleaning: remove the common "..." truncation string
                    cleaned_content = content.split('[+')[0].strip()
                    f.write(cleaned_content + "\n\n")
        
        print(f"Successfully saved {len(all_articles['articles'])} articles to {file_path}")
        return file_path

    except Exception as e:
        print(f"An error occurred while fetching news data: {e}")
        return None