from openai import OpenAI
import os

#client = OpenAI(api_key=os.getenv("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"))

client = OpenAI()

def generate_ai_explanation(ticker, price_insights, sentiment, classification):
    prompt = f"""
You are a professional stock market analyst.

Analyze the following information and produce a clear, neutral explanation.
Do NOT give financial advice. Do NOT say buy or sell.

Stock: {ticker}

Price Insights:
- Price change (2Y): {price_insights['price_change_pct']}%
- 20-day volatility: {price_insights['volatility_20d']}%
- Max drawdown: {price_insights['max_drawdown_pct']}%
- Above 50-day MA: {price_insights['above_50_ma']}
- Above 200-day MA: {price_insights['above_200_ma']}

News Sentiment:
- Average sentiment score: {sentiment['average_sentiment']}
- Overall sentiment: {sentiment['sentiment_label']}

Explain:
1. Overall price trend
2. Risk profile
3. Impact of recent news sentiment
4. Short-term vs long-term considerations

Tone: professional, concise, factual.

Classification Signal: {classification}

Explain WHY this classification makes sense based on price trend, risk, and sentiment.
Clearly state this is informational and not financial advice.

If the asset is a precious metal, explain:
- Role as hedge or safe-haven
- Sensitivity to volatility and macro uncertainty
- Why trends may differ from equities


"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a financial market analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

