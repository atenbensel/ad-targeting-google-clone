import sqlite3

# Connect to the database
conn = sqlite3.connect('tweets.db')
c = conn.cursor()

# Prompt the user to enter keywords to search for (comma separated)
keywords = input("Enter keywords to search for (comma separated): ").split(',')

# Search for tweets containing the keywords
query = "SELECT * FROM tweets WHERE " + " AND ".join(["text LIKE ?" for _ in keywords])
c.execute(query, tuple(f'%{keyword}%' for keyword in keywords))
tweets = c.fetchall()

# Compute the score of each tweet
scores = []
for tweet in tweets:
    # Extract relevant information from the tweet
    text = tweet[1]
    author = tweet[2]
    date = tweet[3]
    verified = tweet[4]
    promoted = tweet[5]

    # Compute the score of the tweet
    K = sum(keyword in text for keyword in keywords)
    m = 1 if K == len(keywords) else 0
    V = 1 if verified else 0
    P = 2 if promoted else 0
    score = K * m + V + P

    # Add the tweet and its score to the scores list
    scores.append((tweet, score))

# Sort the tweets by their score in descending order
sorted_tweets = sorted(scores, key=lambda x: -x[1])

# Display the tweets and their scores
for tweet, score in sorted_tweets:
    text = tweet[1]
    author = tweet[2]
    date = tweet[3]
    promoted = tweet[5]
    print(f'{text} ({author}, {date}){" [PROMOTED]" if promoted else ""}: {score}')

