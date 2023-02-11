from gnewsclient import gnewsclient
from pydantic import BaseModel
import regex as re

class NewsRequest(BaseModel):
    language: str
    location: str

def fetch_news(news_req: NewsRequest) -> list:
    language = news_req.language
    location = news_req.location
    client = gnewsclient.NewsClient(language, location, max_results=5)
    news = client.get_news()
    texts = []
    i = 0
    for text in news:
        texts.append(news[i]["title"])
        # summary = news[i]["summary"]
        # summary_cleaned = re.sub('<[^<]+?>', '', summary)
        # texts.append(summary_cleaned)
        i += 1
    return texts

if __name__ == '__main__':
    news_req = NewsRequest(language="ja", location="ja")
    print(fetch_news(news_req))