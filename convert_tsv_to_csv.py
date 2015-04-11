import os, codecs, csv, datetime, calendar

from Politweet import *

# Date: 9/27/08 of the tweet dataset

if __name__ == "__main__":
    filename = "datasets/tweets.tsv"
    if not os.path.isfile(filename):
        sys.exit("File does not exist.")
    tweets = get_tweets(filename)
    with codecs.open("datasets/tweets.csv", "w", "utf-8") as f:
        for i, tweet in tweets.iterrows():
            #unix_timestamp = str(convert_to_unixtimestamp())
            time = tweet["pub.date.GMT"].split(" ")[1].replace(":", "")
            new_line_list = [time, str(i), " ".join(tweet["tokens"]).strip()]
            f.write(",".join(new_line_list) + "\n")
