from newsapi import NewsApiClient

NEWS_API_KEY = "50430179a76d4550aae5f5d849c612dd"

def fetch_stock_news(ticker, company_name=None, days=7):
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    query = company_name if company_name else ticker

    articles = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="relevancy",
        page_size=10
    )

    return articles["articles"]

