import os
import pandas as pd

if __name__ == "__main__":
    filename = "datasets/tweets.tsv"
    if not os.path.isfile(filename):
        sys.exit("File does not exist.")

    try:
        df = pd.read_csv(
            filename,
            sep='\t',
            encoding='utf-8',
            index_col="tweet.id")

        df.to_csv("datasets/tweets.csv", sep=',', encoding='utf-8')
    except:
        raise
