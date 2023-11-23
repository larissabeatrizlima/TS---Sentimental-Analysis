from GoogleNews import GoogleNews
import pandas as pd
import time

unique_articles = set()


def scrape_google_news(keyword, lang, period='30d'):
    # Initialize GoogleNews
    googlenews = GoogleNews(lang=lang, period=period)
    
    # Search for the keyword
    googlenews.search(keyword)
    
    # Fetch results
    results = googlenews.result()
    print(f"Initial articles found: {len(results)} in language: {lang}")
    for result in results:
        unique_articles.add(result['link'])  # Check link as index for unique news

    # Loop through all pages
    page = 2
    while True:
        googlenews.getpage(page)
        new_results = googlenews.result()

        new_article_found = False

        for result in new_results:
            if result['link'] not in unique_articles:
                unique_articles.add(result['link'])
                results.append(result)
                new_article_found = True

        if not new_article_found:
            print(f"No more new articles. Stopped at page {page}.")
            break

        page += 1
        time.sleep(1)

    # Clear search
    googlenews.clear()
    
    return results

# Define your search term here
search_term = "Ana Benevides"

# Scrape news in Portuguese
news_articles_pt = scrape_google_news(search_term, lang='pt-BR')
df_pt = pd.DataFrame(news_articles_pt)
df_pt.to_csv('google_news_results_pt.csv', index=False)
print(f"Total Portuguese articles retrieved: {len(news_articles_pt)}")

# Scrape news in English
news_articles_en = scrape_google_news(search_term, lang='en')
df_en = pd.DataFrame(news_articles_en)
df_en.to_csv('google_news_results_en.csv', index=False)
print(f"Total English articles retrieved: {len(news_articles_en)}")