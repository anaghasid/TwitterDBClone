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



def like_tweet(tweet_id, user_name):
    print(tweet_id)
    query = f"INSERT INTO Likes_Tweet (user_name, tweet_id) VALUES ('{user_name}', {tweet_id})"
    query2 = f"UPDATE tweet SET num_likes=num_likes+1 WHERE tweet_id={tweet_id}"
    execute_query(query)
    execute_query(query2)

def add_comment(tweet_id, user_name, comment_content):
    query = f"INSERT INTO Comment (tweet_id, commenting_user, comment_content, timestamp) VALUES ({tweet_id}, '{user_name}', '{comment_content}', CURRENT_TIMESTAMP)"
    execute_query(query)


# Function to follow/unfollow a user
def toggle_follow(follower, following, follow):
    query = "INSERT INTO Follows (follower, following) VALUES (%s, %s)" if follow else "DELETE FROM Follows WHERE follower = %s AND following = %s"
    execute_query(query, (follower, following))



def login(username, password):
    query = f"SELECT * FROM user WHERE user_name='{username}'"
    x = execute_query(query)
    print(x)
    if x[0]["user_name"] == username and x[0]["passwd"] == password:
        return x[0]
    return None


# FIX THIS
def register(username, password, first_name):
    query = "INSERT INTO tweet (user_name, password, time_stamp) VALUES (%s, %s, %s)"
    # user_database.append({"username": username, "password": password, "first_name": first_name})





# Main
def main():
    # Create Tweet
    tweet_content = st.text_area("What's happening?")

    if st.button("Tweet"):
        create_tweet("user123", tweet_content)

    st.title("Tweets from your friends")
    tweets = get_tweets()
    for tweet in tweets:
        display_tweet(tweet)
        st.button(f"❤️", key=f"like{tweet['tweet_id']}" on_click=like_tweet, args=(tweet["tweet_id"], user["user_name"]))

        # if st.button("❤️", key=f'like{tweet["tweet_id"]}'):
        #     print("hi",tweet["tweet_id"])
        #     like_tweet(tweet["tweet_id"],user)
        st.divider()
        

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





# Sidebar for login and registration
st.sidebar.title("Login / Register")
action = st.sidebar.radio("Select Action", ["Login", "Register"])

if action == "Login":
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user = login(username, password)
        if user:
            st.success(f"Welcome, {user['first_name']}!")
            main()
        else:
            st.error("Invalid username or password")

elif action == "Register":
    st.subheader("Register")
    new_username = st.sidebar.text_input("New Username")
    first_name = st.sidebar.text_input("First name")
    email = st.sidebar.text_input("Last name")
    new_username = st.sidebar.text_input("Email")
    new_password = st.sidebar.text_input("New Password", type="password")


    if st.sidebar.button("Register"):
        register(new_username, new_password, first_name)
        st.success("Registration successful. You can now login.")