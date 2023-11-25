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
    if st.button(f"**@{tweet['user_name']}**",key=f"{tweet['user_name']}{tweet['tweet_id']}"):
        x = get_tweets_with_users(tweet)
        st.warning(f"User is {x[0]['f_name']} {x[0]['l_name']}. Wish them on {x[0]['bday']}")
        st.warning(f"{x[0]['f_name']} has {x[0]['num_tweets']} tweets")
    st.write(tweet['tweet_content'])
    st.write(f"🕒 {tweet['time_stamp']}")

def get_tweets_with_users(tweet):
    query = f"""
    SELECT t.user_name, u.first_name as f_name, u.last_name as l_name, u.birthday as bday, COUNT(*) as num_tweets
    FROM Tweet t
    JOIN User u ON t.user_name = u.user_name
    WHERE u.user_name = "{tweet['user_name']}"
    GROUP BY t.user_name
    """
    user_tweets = execute_query(query)
    return user_tweets



def like_tweet(tweet_id, user_name):
    print("hello",user)
    query = f"INSERT INTO Likes_Tweet (user_name, tweet_id) VALUES ('{user_name}', {tweet_id})"
    execute_query(query)
    # query2 = f"UPDATE tweet SET num_likes=num_likes+1 WHERE tweet_id={tweet_id}"
    # execute_query(query2)

def add_comment(tweet_id, user_name, comment_content):
    print("in add comment fn",comment_content)
    if comment_content:
        query = f"INSERT INTO Comment (comment_id, tweet_id, commenting_user, comment_content) VALUES (UUID_TO_BIN(UUID()),{tweet_id}, '{user_name}', '{comment_content}')"
        execute_query(query)


# Function to follow/unfollow a user
def toggle_follow(follower, following, follow):
    query = "INSERT INTO Follows (follower, following) VALUES (%s, %s)" if follow else "DELETE FROM Follows WHERE follower = %s AND following = %s"
    execute_query(query, (follower, following))



def login(username, password):
    query = f"SELECT * FROM user WHERE user_name='{username}'"
    x = execute_query(query)
    print(x)
    if x is None:
        return None
    if x[0]["user_name"] == username and x[0]["passwd"] == password:
        return x[0]


# FIX THIS
def register(username, password, first_name):
    query = "INSERT INTO tweet (user_name, password, time_stamp) VALUES (%s, %s, %s)"
    # user_database.append({"username": username, "password": password, "first_name": first_name})

def get_comments(tweet_id):
    query = f"SELECT * FROM comment WHERE tweet_id = {tweet_id} ORDER BY time_stamp"
    comments = execute_query(query)
    return comments


st.title("Twitter")

def main():


    tweet_content = st.text_area("What's happening?")
    if st.button("Tweet"):
        create_tweet(user["user_name"], tweet_content)


    st.title("Tweets")
    tweets = get_tweets()
    for tweet in tweets:
        display_tweet(tweet)

        col1, col2 = st.columns([1,1])
        with col1:
            st.button(f"❤️ {tweet['num_likes']}", key=f"like{tweet['tweet_id']}", on_click=like_tweet, args=(tweet["tweet_id"], user["user_name"]))

        with col2:
            if st.button(f"🗨️ {tweet['num_comments']}", key=f"comment{tweet['tweet_id']}"):
                pass
                # st.button("Comment", on_click=add_comment, args=(tweet["tweet_id"], user["user_name"], comment_content))

        # with col3:
            # if st.button(f"🔁", key=f"retweet{tweet['tweet_id']}"):
            #     pass

        comments = get_comments(tweet["tweet_id"])
        comment_label = "Be the first to comment:"
        if comments:
            comment_label = "Write your comment:"
        
        comment_content = st.text_area(comment_label,key=f"comm_text{tweet['tweet_id']}")
        st.button("Comment", key=f"postcomment{tweet['tweet_id']}", on_click=add_comment, args=(tweet["tweet_id"], user["user_name"], comment_content))

        # show comments if expanded
        if comments:
            my_expander = st.expander(label="Open comments")
            with my_expander:
                for comment in comments:
                    st.write(f"{comment['commenting_user']} commented: {comment['comment_content']}")
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

    any_query = st.text_area(label="Type your own query!")
    if st.button("Execute query"):
        if "SELECT" in any_query:   
            ans = execute_query(any_query)
            st.write(ans)
        else:
            execute_query(any_query)



# user = {'user_name': 'john_doe', 'first_name': 'John', 'last_name': 'Doe', 
#         'passwd': 'abcd', 'email_id': 'john.doe@email.com', 
#         'birthday': '1990-05-15', 'bio': 'I love coding!', 'num_followers': 100, 'num_following': 50}

user = {'user_name': 'priya_1985', 'first_name': 'Priya', 'last_name': 'Sharma', 'passwd': 'samplepass', 
        'email_id': 'priya@gmail.com', 'birthday': '1990-08-22', 
            'bio': 'Travel lover and foodie.', 'num_followers': 150, 'num_following': 100}

main()

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
            print(user)
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

