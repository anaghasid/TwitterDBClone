import streamlit as st
import pandas as pd
import numpy as np
import pymysql
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

# Database Connection
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=os.getenv('PASSWD'),
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
    query = "SELECT * FROM tweet ORDER BY time_stamp DESC LIMIT 10"
    return execute_query(query)

def display_tweet(tweet):
    st.write(f"**@{tweet['user_name']}**")
    st.write(tweet['tweet_content'])
    st.write(f"🕒 {tweet['time_stamp']}   ❤️ {tweet['num_likes']}   🔁 {tweet['num_retweets']}")
    st.divider()

# Display tweets
tweets = get_tweets()
for tweet in tweets:
    display_tweet(tweet)

# User-Following Relationships
st.header("User-Following Relationships")

# Function to follow/unfollow a user
def toggle_follow(follower, following, follow):
    query = "INSERT INTO Follows (follower, following) VALUES (%s, %s)" if follow else "DELETE FROM Follows WHERE follower = %s AND following = %s"
    execute_query(query, (follower, following))






def login(username, password):
    query = "SELECT user_name FROM tweet ORDER BY time_stamp DESC"
    for user in query:
        if user["username"] == username and user["password"] == password:
            return user
    return None


# FIX THIS
def register(username, password, first_name):
    query = "INSERT INTO tweet (user_name, tweet_content, time_stamp) VALUES (%s, %s, %s)"
    # user_database.append({"username": username, "password": password, "first_name": first_name})





# Main
if __name__ == "__main__":


    st.title("Twitter-like App")

    # Sidebar for login and registration
    st.sidebar.title("Login / Register")
    action = st.sidebar.radio("Select Action", ["Login", "Register"])

    if action == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login(username, password)
            if user:
                st.success(f"Welcome, {user['first_name']}!")
            else:
                st.error("Invalid username or password")

    elif action == "Register":
        st.subheader("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        first_name = st.text_input("First Name")

        if st.button("Register"):
            register(new_username, new_password, first_name)
            st.success("Registration successful. You can now login.")
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
