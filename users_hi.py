import streamlit as st
import pandas as pd
import numpy as np
import pymysql
from datetime import datetime


# Database Connection
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='idliPongal1',
                             database='twitter',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# Streamlit App
st.title("Twitter Clone")

# Function to execute SQL queries
def execute_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if "SELECT" in query:
            return cursor.fetchall()
        else:
            connection.commit()

# Tweet Management
st.header("Tweet Management")

# Function to create a tweet
def create_tweet(user_name, tweet_content):
    timestamp = datetime.now()
    query = "INSERT INTO Tweet (user_name, tweet_content, time_stamp) VALUES (%s, %s, %s)"
    execute_query(query, (user_name, tweet_content, timestamp))

# Function to get tweets
def get_tweets():
    query = "SELECT * FROM Tweet ORDER BY time_stamp DESC"
    return execute_query(query)

# Display tweets
tweets = get_tweets()
for tweet in tweets:
    st.write(tweet)

# User-Following Relationships
st.header("User-Following Relationships")

# Function to follow/unfollow a user
def toggle_follow(follower, following, follow):
    query = "INSERT INTO Follows (follower, following) VALUES (%s, %s)" if follow else "DELETE FROM Follows WHERE follower = %s AND following = %s"
    execute_query(query, (follower, following))

# Search
st.header("Search")

# Function to search for users, hashtags, and tweets
def search(query):
    # Implement search logic here
    pass

# Trending Topics
st.header("Trending Topics")

# Function to get trending topics
def get_trending_topics():
    # Implement trending topics logic here
    pass

# Main
if __name__ == "__main__":
    st.sidebar.header("User Actions")

    # Create Tweet
    tweet_content = st.text_area("What's happening?")
    if st.button("Tweet"):
        create_tweet("user123", tweet_content)

    # Follow/Unfollow
    # st.subheader("Follow/Unfollow")
    # follow_user = st.text_input("Follow/Unfollow user:")
    # if st.button("Follow"):
    #     toggle_follow("user123", follow_user, True)
    # if st.button("Unfollow"):
    #     toggle_follow("user123", follow_user, False)

    # # Search
    # st.subheader("Search")
    # search_query = st.text_input("Search:")
    # if st.button("Search"):
    #     search_results = search(search_query)
    #     st.write(search_results)

    # # Trending Topics
    # st.sidebar.subheader("Trending Topics")
    # trending_topics = get_trending_topics()
    # st.sidebar.write(trending_topics)
