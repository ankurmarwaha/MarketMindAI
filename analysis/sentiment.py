from textblob import TextBlob

def analyse_sentiment(articles):
    sentiments = []

    for article in articles:
        text = f"{article.get('title', '')}. {article.get('description', '')}"
        polarity = TextBlob(text).sentiment.polarity
        sentiments.append(polarity)

    if not sentiments:
        return {
            "average_sentiment": 0,
            "sentiment_label": "Neutral"
        }

    avg = sum(sentiments) / len(sentiments)

    if avg > 0.1:
        label = "Positive"
    elif avg < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "average_sentiment": round(avg, 3),
        "sentiment_label": label
    }

