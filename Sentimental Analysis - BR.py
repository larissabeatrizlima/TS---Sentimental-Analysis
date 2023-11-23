import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from deep_translator import GoogleTranslator
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter
import re

### BR news

# Initialize Google Translator and NLTK VADER
#nltk.download('vader_lexicon')
#nltk.download('punkt')

sia = SentimentIntensityAnalyzer()

# Load Portuguese articles
df_pt = pd.read_csv('google_news_results_pt.csv')

try:
    df_pt = pd.read_csv('portuguese_news_sentiment.csv')
except FileNotFoundError:
    def translate_to_english(text):
        translator = GoogleTranslator(source='pt', target='en')
        return translator.translate(text)

    # Function to get sentiment
    def get_sentiment(text):
        translated_text = translate_to_english(text)
        sentiment_score = sia.polarity_scores(translated_text)['compound']
        return sentiment_score

    # Apply translation and sentiment analysis
    df_pt['sentiment'] = df_pt['title'].apply(get_sentiment)

    def categorize_sentiment(score):
        if score > 0.05:
            return 'Positive'
        elif score < -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    df_pt['sentiment_category'] = df_pt['sentiment'].apply(categorize_sentiment)

    df_pt.to_csv('portuguese_news_sentiment.csv', index=False)

# Some EDA process

sns.set_style("whitegrid")
colors = {'Negative': '#EB062F', 'Neutral': '#F77601', 'Positive': '#008140'}

# Plot for Portuguese articles
plt.figure(figsize=(12, 8))
sns.countplot(x='sentiment_category', data=df_pt, palette=colors)
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
df_pt['word_sentiments'] = df_pt.apply(extract_word_sentiments, axis=1)

# Flatten the list of word sentiment tuples
word_sentiments_flat = [item for sublist in df_pt['word_sentiments'] for item in sublist]

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

# Load your DataFrame
df_pt = pd.read_csv('portuguese_news_sentiment.csv')

# Clean the text and apply the N-gram analysis
df_pt['cleaned_text'] = df_pt['title'].apply(clean_text)

# Plot sentiment scores for individual words
plt.figure(figsize=(12, 8))
sns.boxplot(x='word', y='sentiment', data=word_sentiments_df)
plt.title('Sentiment Scores for Individual Words')
plt.xlabel('Words')
plt.ylabel('Sentiment Score')
plt.xticks(rotation=90)
plt.show()

# Get the top unigrams, bigrams, and trigrams
print("Top 10 Unigrams:", get_top_ngrams(df_pt['cleaned_text'], 1))
print("Top 10 Bigrams:", get_top_ngrams(df_pt['cleaned_text'], 2))
print("Top 10 Trigrams:", get_top_ngrams(df_pt['cleaned_text'], 3))

positive_texts = df_pt[df_pt['sentiment_category'] == 'Positive']['cleaned_text']
print("Top 10 Bigrams in Positive Sentiment:", get_top_ngrams(positive_texts, 2))

negative_texts = df_pt[df_pt['sentiment_category'] == 'Negative']['cleaned_text']
print("Top 10 Bigrams in Negative Sentiment:", get_top_ngrams(negative_texts, 2))

neutral_texts = df_pt[df_pt['sentiment_category'] == 'Neutral']['cleaned_text']
print("Top 10 Bigrams in Neutral Sentiment:", get_top_ngrams(neutral_texts, 2))
