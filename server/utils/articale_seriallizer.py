import json

def seriallizer(articles, rm_keys = None):
    processed_articles = []
    for article in articles:
      temp :dict = json.loads(article.to_json())
      
      if (rm_keys != None):
        temp.pop(rm_keys)

      processed_articles.append(temp)
    return processed_articles