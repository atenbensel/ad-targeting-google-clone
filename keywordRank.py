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

# Process the tweets
scores = {}
for tweet in tweets:
    # Extract relevant information from the tweet
    text = tweet[1]
    author = tweet[2]
    date = tweet[3]
    verified = tweet[4]
    promoted = tweet[5]

    # Score the tweet based on its relevance to the keywords and other factors
    score = 0
    if all(keyword in text for keyword in keywords):
        score = len(keywords)
        if verified:
            score += 1
        if promoted:
            score += 2

    # Add the tweet and its score to the scores dictionary
    scores[tweet] = score

# Sort the tweets by their score, with promoted tweets first
sorted_tweets = sorted(scores.items(), key=lambda x: (-x[1], -x[0][3], -x[0][0]))

# Display the tweets and their scores
for tweet, score in sorted_tweets:
    text = tweet[1]
    author = tweet[2]
    date = tweet[3]
    verified = tweet[4]
    promoted = tweet[5]
    print(f'{text} ({author}, {date}){" [PROMOTED]" if promoted else ""}: {score}')
