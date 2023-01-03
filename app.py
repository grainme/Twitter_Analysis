import tweepy
import nltk
nltk.download('vader_lexicon')
from flask import Flask, render_template, request

app = Flask(__name__)

from nltk.sentiment.vader import SentimentIntensityAnalyzer
    
def nltk_sent(tweet):


    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Use the analyzer to get the sentiment scores for the tweet
    scores = analyzer.polarity_scores(tweet)

    # Determine the overall sentiment of the tweet
    if scores['compound'] > 0:
        return "Positive"
    elif scores['compound'] < 0:
        return "Negative"
    else:
        return "Neutral"
        

result = []
# insert your Twitter API keys and access tokens here
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_token_secret = 'access_token_secret'

# Authenticate with the Twitter API using the API keys and access tokens
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)

# Create an API client using the authenticated handler
api = tweepy.API(auth)



@app.route("/", methods = ["GET", "POST"])
def home():
    return render_template("home.html")

        
@app.route("/home", methods = ["GET","POST"])
def main_page():
    screen_name = request.form.get("screen_name")
    # Fetch the user's tweets using the API client
    tweets = api.user_timeline(screen_name=screen_name, count=8)


    # Iterate over each tweet and perform sentiment analysis
    result = []
    for tweet in tweets:
        # Extract the relevant data from the tweet object
        created_at = tweet.created_at
        text = tweet.text
        likes = tweet.favorite_count

        d = {
            "created at": created_at,
            "text": text,
            "likes": likes,
            "sentiment": nltk_sent(text),
        }
        result.append(d)
        
    return render_template("index.html", tweets = result)



if __name__ == "__main__":
    app.run(debug=True)
