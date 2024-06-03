
    # Analyze sentiment of posts
    for post in posts:
        content = post['title'] + ' ' + post['text']
        analysis = TextBlob(content)
        post['sentiment'] = analysis.sentiment.polarity
        post['sentiment_label'] = 'Positive' if analysis.sentiment.polarity > 0 else 'Neutral' if analysis.sentiment.polarity == 0 else 'Negative'
    return posts

def display_results(posts, df, subreddit, keyword):
    # Create a figure with subplots
    fig, axs = plt.subplots(2, 1, figsize=(5, 10))  # Adjusted figure size

    # Pie chart for sentiment
    sentiment_counts = df['sentiment_label'].value_counts().reindex(["Positive", "Neutral", "Negative"], fill_value=0)