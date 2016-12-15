from nltk.tokenize import TweetTokenizer

twtokenizer = TweetTokenizer(preserve_case=True, strip_handles=True, reduce_len=True)

def tweet_tokenize(msg):
    return twtokenizer.tokenize(msg)