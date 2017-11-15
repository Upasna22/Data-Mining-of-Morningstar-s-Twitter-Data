import tweepy
import csv
import pandas as pd
import sys
import re
import codecs
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import operator
import pprint

reload(sys)  
sys.setdefaultencoding('utf8')

####input your credentials here
consumer_key = 'Ws8xWBgnK7lX0nBVT6y7q9Cae'
consumer_secret = 'zFolUSJa89DCA1zjYKyZpj456SMaJxHXyzNRCSCNkwFtFlGBZi'
access_token = '635142863-tvusjpS4iCk2AbRTT21rlZD7OEA9C5ZJLXp1gfqf'
access_token_secret = 'b3C7vRNHwGvhwgvnDi9F6seOh6KCRrNgnX5xVh8hH9qw0'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Open/Create a file to append data
csvFile = open('mstar7.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

search_terms =('Morningstar.com OR Morningstar rating ')
for tweet in tweepy.Cursor(api.search,q=search_terms,count=1000,
                           lang="en",
                           since="2014-01-01").items():
    csvWriter.writerow([tweet.text.encode('utf-8')])

def processTweet(tweet): 
    # strip 
    tweet = tweet.strip()
    #first convert to lower case
    tweet = tweet.lower()
    #converting @username to AT_USER eg : @ParamourWayne => AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    # replace "#word" with "word"
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    return tweet

##stopwords
def getStopWordList():
    stopWords=[]
    stopWords.append('at_user')
    stopWords.append('url')

    file = open(sys.argv[1])
    for line in file:
        stop_word = line.strip()
        stopWords.append(stop_word)
    return stopWords;

stopWords =[]
stopWords = getStopWordList()

#look for characters with 2 or more repititions and replace with character itself
def replaceTwoOrMoreChars(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

def getFeatures(tweet):
    featureVector = []
    pos_words=[]
    neg_words=[]
    neutral_words=[]
    # tokenize tweets
    tweet = processTweet(tweet)
    for w in tweet.split():
        #strip punctuation 
        w = w.strip('\'"?,.')
        #replacing two or chars 
        w = replaceTwoOrMoreChars(w)
        #check if word starts with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        w = w.lower()
        # remove stop words
        if(w not in stopWords):
            featureVector.append(w)
    return featureVector
       
tweet_file = open('mstar7.csv','r')
feature_list=[]
for line in tweet_file:
    line = unicode(line, errors='ignore')
    feature_list.append(getFeatures(line))


def getSentimentScores(feature_list):
    sentiment_list={}
    count =0
    for list in feature_list:
        count = count + 1
        sentence = ' '.join(list)
        sentence_blob = TextBlob(sentence)
        sentence_sentiment = sentence_blob.sentiment.polarity
        #print sentence+"____________:",sentence_sentiment
        sentiment_list[sentence] = sentence_sentiment
    #print count
    return sentiment_list
    
    
sentiment_list={}
sentiment_list = getSentimentScores(feature_list)

def getRelevantTweets(sentiment_list):
    sorted(sentiment_list.values(),reverse=True)
    #print len(sentiment_list)
    for key in sentiment_list.keys():
        if 'at_user' in key:
            del sentiment_list[key]
    #sentiment_list={key: value for key, value in sentiment_list.items() 
    #         if 'at_user' not in key}
    #print len(sentiment_list)
    sorted_sentiment_list_asc=[(k,v) for v,k in sorted(
        [(v,k) for k,v in sentiment_list.items()])
    ]
    sorted_sentiment_list=[(k,v) for v,k in sorted(
        [(v,k) for k,v in sentiment_list.items()], reverse=True)
    ]
    print 'Top 10 positive tweets are : \n'
    pprint.pprint(sorted_sentiment_list[:10])
    print 'Top 10 negative tweets are : \n'
    pprint.pprint(sorted_sentiment_list_asc[:10])

getRelevantTweets(sentiment_list)

def getSentimentGraph(sentiment_list):
    pos_tweets =[]
    neg_tweets=[]
    neutral_tweets=[]
    sentiments=[]
    for key in sentiment_list:
        if(sentiment_list[key] > 0.0):
            pos_tweets.append(key)
        elif(sentiment_list[key] < 0.0):
            neg_tweets.append(key)
        else:
            neutral_tweets.append(key)
    
    objects = ("Positive","Negative","Neutral")
    y_pos = np.arange(len(objects))
    lengthOfSentiments = [len(pos_tweets),len(neg_tweets),len(neutral_tweets)]
    plt.bar(y_pos, lengthOfSentiments, align ='center', alpha =0.5)
    plt.xticks(y_pos, objects)
    plt.title('No of tweets vs Sentiment')
    plt.xlabel('Number of Tweets')
    plt.ylabel('Mood')
    plt.show()
    sentiments=list(sentiment_list.values())
    plt.plot(sentiments, marker='o', linestyle='--', color='r')
    plt.ylabel('sentiment values')
    plt.title('Sentiment values of relevant tweets')
    plt.show()
getSentimentGraph(sentiment_list)


def getWordCloud(tweet_file):
    pos_words=[]
    neg_words=[]
    neutral_words=[]
    word_count =0
    unwanted_words=['https','rt']
    for tweet in tweet_file:
        tweet = processTweet(tweet)
        for word in tweet.split():
            word_count = word_count + 1
            word = word.lower()
            if word not in stopWords:
                word_blob = TextBlob(word)
                sentiment = word_blob.sentiment.polarity
                if(sentiment > 0.0):
                    pos_words.append(word)
                elif(sentiment < 0.0):
                    neg_words.append(word)
                else:
                    if word not in unwanted_words:
                        neutral_words.append(word)
    print 'Number of positive words = ', len(pos_words), '/', word_count,'\n'
    print 'Number of negative words = ',len(neg_words),'/',word_count,'\n'
    print 'Number of neutral words = ',len(neutral_words),'/',word_count,'\n'
    pos_sentence=' '.join(pos_words)
    neg_sentence=' '.join(neg_words)
    neutral_sentence=' '.join(neutral_words)
    wordcloud_pos = WordCloud(background_color='black', width=2500, height=2000).generate(pos_sentence)
    plt.figure(1,figsize=(13,13))
    plt.imshow(wordcloud_pos)
    plt.axis('off')
    plt.title('Positive WordCloud')
    plt.show()
    wordcloud_neg = WordCloud(background_color='black', width=2500, height=2000).generate(neg_sentence)
    plt.figure(1,figsize=(13,13))
    plt.imshow(wordcloud_neg)
    plt.axis('off')
    plt.title('Negative WordCloud')
    plt.show()
    wordcloud_neutral = WordCloud(background_color='black', width=2500, height=2000).generate(neutral_sentence)
    plt.figure(1,figsize=(13,13))
    plt.imshow(wordcloud_neutral)
    plt.axis('off')
    plt.title('Neutral WordCloud')
    plt.show()



file_tweet = open('mstar7.csv','r')
getWordCloud(file_tweet)



