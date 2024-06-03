import praw
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


reddit = praw.Reddit(client_id='CYHLSUHNMc_9rpXz8E9lNQ',
                     client_secret='4JepsnzbpppouK0E0uM4a6GPOMlTSg',
                     user_agent='console:Sentiment:1.0')

def fetch_posts(subreddit, keyword):
    posts = []
    for submission in reddit.subreddit(subreddit).search(keyword, limit=100):
        posts.append({'title': submission.title, 'text': submission.selftext})
    return posts

def analyze_sentiment(posts):
    for post in posts:
        content = post['title'] + ' ' + post['text']
        analysis = TextBlob(content)
        post['sentiment'] = analysis.sentiment.polarity
        post['sentiment_label'] = 'Positive' if analysis.sentiment.polarity > 0 else 'Neutral' if analysis.sentiment.polarity == 0 else 'Negative'
    return posts

def display_results(posts, df, subreddit, keyword):
    fig, axs = plt.subplots(2, 1, figsize=(5, 10))  # Adjusted figure size
    #pie chart
    sentiment_counts = df['sentiment_label'].value_counts().reindex(["Positive", "Neutral", "Negative"], fill_value=0)
    colors = ['#77dd77', '#779ecb', '#ff6961'] 
    axs[0].pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
    axs[0].axis('equal') 
    axs[0].set_title(f'Sentiment Analysis of "{keyword}" in r/{subreddit}')

    #word cloud
    text = ' '.join(post['title'] + ' ' + post['text'] for post in posts)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    axs[1].imshow(wordcloud, interpolation='bilinear')
    axs[1].axis('off')
    axs[1].set_title(f'Word Cloud for "{keyword}" in r/{subreddit}')

    plt.tight_layout(pad=5) #padding for overlap
    plt.show()

    sorted_df = df.sort_values(by='sentiment', ascending=False)
    print("\nSorted posts by sentiment:")
    for _, row in sorted_df.iterrows():
        print(f"Sentiment: {row['sentiment_label']}, Post Title: {row['title']}")

def main():
    subreddit_name = input("Enter a subreddit name: ")
    search_term = input("Enter a search term: ")

    posts = fetch_posts(subreddit_name, search_term)
    if not posts:
        print("No posts found with the given search term in the specified subreddit.")
        return

    analyzed_posts = analyze_sentiment(posts)

    df = pd.DataFrame(analyzed_posts)

    display_results(posts, df, subreddit_name, search_term)

if __name__ == "__main__":
    main()