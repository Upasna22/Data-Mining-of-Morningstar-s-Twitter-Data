# Data-Mining-of-Morningstar-s-Twitter-Data


•	Sentiment Analysis is the process of determining whether a piece of writing is positive, negative or neutral.
•	Marketers can use sentiment analysis to research public opinion of their company and products, or to analyze customer satisfaction and to get critical feedback about their products.
•	Without using any NLTK libraries for text processing or any Machine Learning classifiers for classification, wanted to use my own algorithm for text exploration.


Steps :
1)	Crawl/extract tweets from Twitter with a query string. Here I used Morningstar.com OR Morningstar rating.

2)	Preprocessing data (remove stops words , punctuations etc)
3)	Attribute selection / Extracting Features (used Unigrams)
4)	Assigning a sentiment(value that indicates how positive or negative a word is) for each tweet 
5)	Classification algorithm
6)	 Plots.

Plot 1 – plot of how many of the overall tweets conveyed a positive, negative and neutral sentiment. The emotions of the tweets are greatly skewed towards positive.

Plot 2 – Exact sentiment values of tweets . Tweets were classified as sentiment score > 0.0 – positive , score < 0.0 negative and neutral for 0.0

Plot 3 – wordcloud of the most frequent positive words that appeared in majority of the tweets.

Plot 4 – wordlcloud of the most frequent negative words.

Plot 5 – wordcloud of all the neutral words.

The clouds give greater prominence to words that appear more frequently in the source text.

