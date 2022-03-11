from textblob import TextBlob


def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity


if __name__ == '__main__':
    print(get_sentiment("Hello you son of a bitch."))
