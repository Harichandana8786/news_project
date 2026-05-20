from sqlalchemy import create_engine
from sqlalchemy import text

from modules.config import (
    DB_HOST,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_PORT
)

# =====================================
# DATABASE CONNECTION
# =====================================

DATABASE_URL = (
    f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def save_to_rds(processed_articles):

    create_table_query = """
    CREATE TABLE IF NOT EXISTS news_sentiment (
        id SERIAL PRIMARY KEY,
        title TEXT,
        source TEXT,
        published_at TEXT,
        url TEXT,
        sentiment TEXT,
        sentiment_score FLOAT
    );
    """

    insert_query = text("""
        INSERT INTO news_sentiment (
            title,
            source,
            published_at,
            url,
            sentiment,
            sentiment_score
        )
        VALUES (
            :title,
            :source,
            :published_at,
            :url,
            :sentiment,
            :sentiment_score
        )
    """)

    with engine.begin() as connection:

        # Create table
        connection.execute(text(create_table_query))

        # Insert records
        for article in processed_articles:

            connection.execute(
                insert_query,
                {
                    "title": article["title"],
                    "source": article["source"],
                    "published_at": article["published_at"],
                    "url": article["url"],
                    "sentiment": article["sentiment"],
                    "sentiment_score": article["sentiment_score"]
                }
            )

    print("Data saved successfully")