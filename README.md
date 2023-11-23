# Sentiment Analysis of News Coverage on Taylor Swift Concert Incident

## Project Overview
This project aims to analyze the sentiment in news coverage related to a tragic incident at a Taylor Swift concert, where a fan passed away. The focus of this analysis is to understand how the news is portrayed in local versus foreign media.

## Objective
Much has been discussed regarding the incident at the Taylor Swift concert, with a prominent focus on the contrasting narratives between foreign media and local news. The aim of this study is to examine news headlines and identify any substantial differences in the narratives presented.

## Methodology
- Data Collection: News articles from both local and foreign media outlets covering the event were collected.
- Sentiment Analysis: Using advanced natural language processing techniques, we analyzed the sentiment of the news headlines. The sentiments were categorized as Positive, Neutral, or Negative.
- Comparative Analysis: The results were compared to identify any notable differences in the sentiment between local and foreign news reports.

## Findings

### The Brazilian Media

#### Top 10 Trigrams - Analysis

1. `('de', 'taylor', 'swift')`: 323 occurrences
2. `('show', 'de', 'taylor')`: 147 occurrences
3. `('de', 'ana', 'benevides')`: 128 occurrences
4. `('em', 'show', 'de')`: 101 occurrences
5. `('fã', 'de', 'taylor')`: 78 occurrences
6. `('que', 'morreu', 'em')`: 74 occurrences
7. `('morreu', 'em', 'show')`: 74 occurrences
8. `('família', 'de', 'ana')`: 74 occurrences
9. `('ana', 'clara', 'benevides')`: 71 occurrences
10. `('morte', 'de', 'fã')`: 68 occurrences

#### Sentimental Analysis
![Sentiment Distribuition of BR News](https://miro.medium.com/v2/resize:fit:720/format:webp/1*Cd8p_2aph9AJaTuNjHRdQw.png)

### Foreign Media

#### Top 10 Trigrams - Analysis

1. `('taylor', 'swift', 'fan')`: 51 occurrences
2. `('ana', 'clara', 'benevides')`: 42 occurrences
3. `('fan', 'who', 'died')`: 29 occurrences
4. `('who', 'died', 'at')`: 27 occurrences
5. `('swift', 'fan', 'who')`: 19 occurrences
6. `('taylor', 'swift', 'concert')`: 18 occurrences
7. `('of', 'taylor', 'swift')`: 17 occurrences
8. `('taylor', 'swift', 'fans')`: 16 occurrences
9. `('swift', 'fan', 'dies')`: 16 occurrences
10. `('fan', 'dies', 'at')`: 16 occurrences

#### Sentimental Analysis
![Sentiment Distribuition of English based News](https://miro.medium.com/v2/resize:fit:720/format:webp/1*2mbDA_9EuJZgJJLwg-iL7Q.png)

### Conclusions
Relying solely on article titles makes it difficult to spot differences in narratives between foreign media and local news, as both mostly use similar trigrams in their titles. However, the local news presents a narrative that emphasizes the victim's family, occurring 74 times, while foreign coverage tends to reduce the victim to a generic 'Taylor Swift fan.'

The sentiment analysis doesn't provide significant insights either, as it focuses on the incident, resulting in negative scores for all keywords. This could potentially lead us to a misleading analysis.