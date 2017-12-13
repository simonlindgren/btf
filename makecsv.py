import sqlite3
import pandas as pd
pd.set_option('display.max_colwidth', -1)

# Read sqlite query results into a pandas DataFrame
conn = sqlite3.connect("tweets.db")
tweets_df = pd.read_sql_query("SELECT * from tweets", conn)

tweets_df = tweets_df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
tweets_df = tweets_df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
tweets_df = tweets_df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe

tweets_df.to_csv("tweets.csv")

print("Data saved to tweets.csv!")
