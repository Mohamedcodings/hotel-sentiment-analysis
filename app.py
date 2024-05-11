import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Matplotlib
import matplotlib.pyplot as plt
from flask import Flask, render_template
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import base64
from io import BytesIO

app = Flask(__name__)

def compute_sentiment(data, keywords):
    sia = SentimentIntensityAnalyzer()
    for keyword in keywords:
        # Append '_pos' to store positive sentiment scores
        data[f'{keyword}_pos'] = data['Positive'].apply(lambda x: sia.polarity_scores(x)['compound'] if keyword in x else 0)
        # Append '_neg' to store negative sentiment scores
        data[f'{keyword}_neg'] = data['Negative'].apply(lambda x: sia.polarity_scores(x)['compound'] if keyword in x else 0)
    return data

def plot_enhanced_sentiment(data, keywords):
    plt.figure(figsize=(14, 7))
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    for i, keyword in enumerate(keywords):
        net_sentiment = data[f'{keyword}_pos'] - data[f'{keyword}_neg']
        plt.plot(data['Date'], net_sentiment.rolling(window=7).mean(), label=f'{keyword.capitalize()} Sentiment', color=colors[i % len(colors)])

    plt.axhline(y=0, color='gray', linestyle='--')  # Add a line at zero for reference
    plt.title('Net Sentiment Over Time for All Keywords')
    plt.xlabel('Date')
    plt.ylabel('Net Sentiment Score')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode('utf-8')

def generate_advanced_recommendations(data, keywords):
    recommendations = []
    for keyword in keywords:
        net_sentiment = data[f'{keyword}_pos'] - data[f'{keyword}_neg']
        rolling_net = net_sentiment.rolling(window=7).mean()

        # Check for significant decline
        if rolling_net.pct_change().iloc[-1] < -0.2:  # If there's a significant percentage drop recently
            recommendations.append(f"Significant drop in {keyword} sentiment detected. Investigate potential causes and consider customer outreach for feedback.")

        # Long-term negative trend
        if rolling_net.mean() < 0:
            recommendations.append(f"Overall negative trend in {keyword}. Review operational practices and customer service approaches.")

        # Improvement needed but not urgent
        if rolling_net.iloc[-1] < 0 and rolling_net.iloc[-1] > -0.2:
            recommendations.append(f"Minor concerns in {keyword}. Consider enhancing this area with minor improvements.")

        # Positive trend, encourage maintenance
        if rolling_net.iloc[-1] > 0.2:
            recommendations.append(f"{keyword.capitalize()} is performing well. Maintain high standards and monitor for consistent performance.")

    return recommendations


@app.route('/')
def index():
    data = pd.read_excel('data.xlsx')
    data['Date'] = pd.to_datetime(data['Date'])
    data['Positive'] = data['Positive'].astype(str).str.lower().str.replace('[^\w\s]', '', regex=True)
    data['Negative'] = data['Negative'].astype(str).str.lower().str.replace('[^\w\s]', '', regex=True)
    
    keywords = ['pool', 'breakfast', 'room', 'service', 'staff']
    data = compute_sentiment(data, keywords)
    
    plot_url = plot_enhanced_sentiment(data, keywords)
    recommendations = generate_advanced_recommendations(data, keywords)
    
    return render_template('index.html', plot_url=plot_url, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
