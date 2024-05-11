# Hotel Sentiment Analysis Dashboard

## Overview

The Hotel Sentiment Analysis Dashboard is a Flask-based web application that offers a dynamic overview of customer sentiments across various hotel services such as the pool, breakfast, room, service, and staff. It utilizes Natural Language Processing (NLP) to analyze customer feedback and visualize sentiment trends, helping hotel management to identify areas of improvement and maintain high standards of customer satisfaction.

## Features

- **Sentiment Analysis**: Processes textual feedback to calculate and visualize the net sentiment (positive or negative) across different hotel service categories.
- **Trend Visualization**: Displays sentiment trends over time, allowing users to track how changes in service quality or customer perception impact overall sentiment.
- **Actionable Recommendations**: Generates automated, actionable recommendations based on sentiment trends to guide managerial decisions.

## How It Works

The application integrates several Python libraries to perform its tasks:
- **Flask** serves the application and manages routing and web interactions.
- **Pandas** is used for data manipulation and analysis.
- **Matplotlib** provides the tools to create visualizations of the sentiment data.
- **NLTK** (Natural Language Toolkit) is used for processing textual data to compute sentiment scores.

The application processes input data from an Excel file containing customer feedback, analyzes the sentiment for categorized keywords (like 'pool', 'room', etc.), and then visualizes these sentiments over time. It dynamically generates recommendations based on the analysis, which are displayed on the dashboard.

