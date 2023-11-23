import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter
import re

## For English News

# Download VADER lexicon
#nltk.download('vader_lexicon')

# Initialize VADER
sia = SentimentIntensityAnalyzer()

# Load English articles
df_en = pd.read_csv('google_news_results_en.csv')

try:
    df_en = pd.read_csv('english_news_sentiment.csv')
except FileNotFoundError:
    df_en['sentiment'] = df_en['title'].apply(lambda title: sia.polarity_scores(title)['compound'])

    def categorize_sentiment(score):
        if score > 0.05:
            return 'Positive'
        elif score < -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    df_en['sentiment_category'] = df_en['sentiment'].apply(categorize_sentiment)

    df_en.to_csv('english_news_sentiment.csv', index=False)

# Some EDA process

sns.set_style("whitegrid")
colors = {'Negative': '#EB062F', 'Neutral': '#F77601', 'Positive': '#008140'}

# Plot for Portuguese articles
plt.figure(figsize=(12, 8))
sns.countplot(x='sentiment_category', data=df_en, palette=colors)
plt.title('Sentiment Distribution of BR News')
plt.xlabel('Sentiment Category')
plt.ylabel('Number of Articles')

# Customization to hide axes and show labels
ax = plt.gca()
for spine in ax.spines.values():
    spine.set_visible(False)
ax.xaxis.set_ticks_position('none') 
ax.yaxis.set_ticks_position('none')

plt.show()

# Function to extract words and their corresponding sentiment scores
def extract_word_sentiments(row):
    words = word_tokenize(row['title'])
    return [(word, row['sentiment']) for word in words]

# Apply the function to create a new column 'word_sentiments'
df_en['word_sentiments'] = df_en.apply(extract_word_sentiments, axis=1)

# Flatten the list of word sentiment tuples
word_sentiments_flat = [item for sublist in df_en['word_sentiments'] for item in sublist]

# Convert the flattened list to a DataFrame
word_sentiments_df = pd.DataFrame(word_sentiments_flat, columns=['word', 'sentiment'])

word_sentiments_df.to_csv('word_sentiments_df_br.csv')

# Define the text cleaning function
def clean_text(text):
    """Clean and preprocess the text."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

# Define the function to generate n-grams
def generate_ngrams(text, n):
    """Generate n-grams from text."""
    words = word_tokenize(text)
    return list(ngrams(words, n))

# Define the function to get top n-grams
def get_top_ngrams(corpus, n, top_k=10):
    """Get the most common n-grams in the corpus."""
    n_grams = []
    for text in corpus:
        n_grams.extend(generate_ngrams(text, n))
    n_gram_freq = Counter(n_grams)
    return n_gram_freq.most_common(top_k)

# Clean the text and apply the N-gram analysis
df_en['cleaned_text'] = df_en['title'].apply(clean_text)

# Plot sentiment scores for individual words
plt.figure(figsize=(12, 8))
sns.boxplot(x='word', y='sentiment', data=word_sentiments_df)
plt.title('Sentiment Scores for Individual Words')
plt.xlabel('Words')
plt.ylabel('Sentiment Score')
plt.xticks(rotation=90)
plt.show()

# Get the top unigrams, bigrams, and trigrams
print("Top 10 Unigrams:", get_top_ngrams(df_en['cleaned_text'], 1))
print("Top 10 Bigrams:", get_top_ngrams(df_en['cleaned_text'], 2))
print("Top 10 Trigrams:", get_top_ngrams(df_en['cleaned_text'], 3))

positive_texts = df_en[df_en['sentiment_category'] == 'Positive']['cleaned_text']
print("Top 10 Bigrams in Positive Sentiment:", get_top_ngrams(positive_texts, 2))

negative_texts = df_en[df_en['sentiment_category'] == 'Negative']['cleaned_text']
print("Top 10 Bigrams in Negative Sentiment:", get_top_ngrams(negative_texts, 2))

neutral_texts = df_en[df_en['sentiment_category'] == 'Neutral']['cleaned_text']
print("Top 10 Bigrams in Neutral Sentiment:", get_top_ngrams(neutral_texts, 2))
