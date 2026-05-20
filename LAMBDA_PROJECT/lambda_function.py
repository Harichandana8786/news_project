import json

from modules.fetch_news import fetch_news
from modules.sentiment_analysis import analyze_sentiment
from modules.database import save_to_rds
from modules.s3_storage import save_to_s3


def lambda_handler(event, context):

    try:

        print("Lambda started")

        # =====================================
        # FETCH NEWS
        # =====================================

        print("Fetching news...")

        news_data = fetch_news()

        print("News fetched successfully")

        # =====================================
        # SAVE RAW JSON TO S3
        # =====================================

        print("Uploading raw JSON to S3...")

        save_to_s3(news_data)

        print("Saved raw JSON to S3")

        # =====================================
        # PROCESS ARTICLES
        # =====================================

        articles = news_data.get("articles", [])

        print(f"Total articles fetched: {len(articles)}")

        processed_articles = []

        for article in articles:

            if not isinstance(article, dict):
                continue

            title = article.get("title", "")

            if not title:
                continue

            # =====================================
            # SENTIMENT ANALYSIS
            # =====================================

            sentiment, score = analyze_sentiment(title)

            processed_article = {
                "title": title,
                "source": article.get("source", {}).get("name", ""),
                "published_at": article.get("publishedAt", ""),
                "url": article.get("url", ""),
                "sentiment": sentiment,
                "sentiment_score": score
            }

            processed_articles.append(processed_article)

        print(f"Processed articles: {len(processed_articles)}")

        # =====================================
        # SAVE TO RDS
        # =====================================

        print("Saving data to PostgreSQL RDS...")

        save_to_rds(processed_articles)

        print("Data inserted successfully")

        return {
            "statusCode": 200,
            "body": json.dumps(
                "News Sentiment Pipeline Executed Successfully!"
            )
        }

    except Exception as e:

        print("ERROR:")
        print(str(e))

        return {
            "statusCode": 500,
            "body": str(e)
        }