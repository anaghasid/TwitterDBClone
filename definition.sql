-- definition: table creation
CREATE TABLE user(
    user_name varchar(20) PRIMARY KEY,
    first_name varchar(20) NOT NULL,
    last_name varchar(20),
    email_id varchar(226) NOT NULL,
    birthday date,
    bio text,
    num_followers int DEFAULT 0,
    num_following int DEFAULT 0
);

CREATE TABLE tweet (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(20) NOT NULL,
    tweet_content TEXT,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    num_likes INT DEFAULT 0,
    num_retweets INT DEFAULT 0,
    FOREIGN KEY (user_name) REFERENCES user(user_name)
);


-- manipulation: inserting values
INSERT INTO user (user_name, first_name, last_name, email_id, birthday, bio, num_followers, num_following)
VALUES
    ('john_doe', 'John', 'Doe', 'john.doe@email.com', '1990-05-15', 'I love coding!', 100, 50),
    ('jane_smith', 'Jane', 'Smith', 'jane.smith@email.com', '1985-08-22', 'Travel enthusiast', 200, 75),
    ('bob_jones', 'Bob', 'Jones', 'bob.jones@email.com', '1995-02-10', 'Coffee addict ☕', 50, 30);

INSERT INTO Tweet (user_name, tweet_content, num_likes, num_retweets)
VALUES
    ('john_doe', 'This is my first tweet!', 10, 5),
    ('bob_jones', 'Hello Twitter! #FirstTweet', 15, 8),
    ('jane_smith', 'Coding all day! #ProgrammerLife', 20, 12),
    ('john_doe', 'I love DBMS!', 25, 18),
    ('jane_smith', 'Traveling to new places', 30, 25);