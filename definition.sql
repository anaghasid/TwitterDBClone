-- definition: table creation
CREATE TABLE user(
    user_name varchar(20) PRIMARY KEY,
    first_name varchar(20) NOT NULL,
    last_name varchar(20),
    passwd varchar(30) NOT NULL,
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

CREATE TABLE comment (
    comment_id binary(16) PRIMARY KEY,
    tweet_id int,
    commenting_user varchar(20),
    comment_content text,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (commenting_user) REFERENCES user(user_name),
    FOREIGN KEY (tweet_id) REFERENCES tweet(tweet_id)
);

CREATE TABLE Likes_Tweet (
    user_name VARCHAR(255),
    tweet_id INT,
    PRIMARY KEY (user_name, tweet_id),
    FOREIGN KEY (user_name) REFERENCES user(user_name),
    FOREIGN KEY (tweet_id) REFERENCES tweet(tweet_id)
);


CREATE TABLE Retweet (
    retweet_id INT PRIMARY KEY AUTO_INCREMENT,
    retweeting_user VARCHAR(255) NOT NULL,
    original_tweet_id INT NOT NULL,
    retweet_content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (original_tweet_id) REFERENCES tweet(tweet_id),
    FOREIGN KEY (retweeting_user) REFERENCES user(user_name)
);

CREATE TABLE Likes_Comment (
    liking_user VARCHAR(255),
    comment_id binary(16),
    PRIMARY KEY (liking_user, comment_id),
    FOREIGN KEY (liking_user) REFERENCES user(user_name),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id)
);

CREATE TABLE Hashtag (
    hashtag_name VARCHAR(255) PRIMARY KEY,
    num_posts INT DEFAULT 0
);

CREATE TABLE Follows (
    ufollower VARCHAR(255),
    ufollowing VARCHAR(255),
    PRIMARY KEY (ufollower, ufollowing),
    FOREIGN KEY (ufollower) REFERENCES user(user_name),
    FOREIGN KEY (ufollowing) REFERENCES user(user_name)
);

-- insert into table waste VALUES (UUID_TO_BIN(UUID()), 20)


-- manipulation: inserting values
INSERT INTO user (user_name, first_name, last_name, email_id, passwd, birthday, bio, num_followers, num_following)
VALUES
    ('john_doe', 'John', 'Doe', 'john.doe@email.com', 'abcd','1990-05-15', 'I love coding!', 0, 0),
    ('jane_smith', 'Jane', 'Smith', 'jane.smith@email.com', 'wanderlust', '1985-08-22', 'Travel enthusiast', 0, 0),
    ('bob_jones', 'Bob', 'Jones', 'bob.jones@email.com','bobbybrew', '1995-02-10', 'Coffee addict ☕', 0, 0)
    ('raj_1990', 'Raj', 'Kumar', 'raj@gmail.com', 'rajhi','1990-05-15', 'Passionate coder and tech enthusiast.', 0, 0),
    ('priya_1985', 'Priya', 'Sharma', 'priya@gmail.com', 'samplepass', '1985-08-22', 'Travel lover and foodie.', 0, 0),
    ('anu_1995', 'Anushka', 'Singh', 'anu@gmail.com', 'anu123', '1995-02-10', 'Movie buff and aspiring artist.', 0, 0);

INSERT INTO Tweet (user_name, tweet_content, num_likes, num_comments)
VALUES
    ('john_doe', 'This is my first tweet!', 0, 0),
    ('bob_jones', 'Hello Twitter! #FirstTweet', 0, 0),
    ('jane_smith', 'Coding all day! #ProgrammerLife', 0, 0),
    ('john_doe', 'I love DBMS!', 0, 0),
    ('jane_smith', 'Traveling to new places', 0, 0)
    ('raj_1990', 'Just finished a coding marathon. Feeling accomplished! #coding #developer', 0, 0),
    ('priya_1985', 'Exploring the streets of Mumbai today. Such a vibrant city! #travel #Mumbai', 0, 0),
    ('anu_1995', 'Art is the expression of the soul. Here`s my latest creation. #art #creativity', 0, 0 );

INSERT INTO comment (comment_id, tweet_id, commenting_user, comment_content)
VALUES
    (UUID_TO_BIN(UUID()), 1, 'jane_smith', 'I love coding too! It is amazing'),
    (UUID_TO_BIN(UUID()), 8, 'raj_1990', 'Great tweet! Totally agree.'),
    (UUID_TO_BIN(UUID()), 8, 'priya_1985', 'Interesting thoughts. Keep it up!'),
    (UUID_TO_BIN(UUID()), 6, 'anu_1995', 'Congratulations! Keep coding');

INSERT INTO Retweet (retweeting_user, original_tweet_id, retweet_content) 
VALUES 
    ('raj_1990', 2, 'Hey Twitter! I am reposting'),
    ('bob_jones', 4, 'I love DBMS too'),
    ('jane_smith', 3, 'With Priya in Mumbai :)');

-- Insert values into Likes_Tweet table
INSERT INTO Likes_Tweet (user_name, tweet_id) 
VALUES 
    ('anu_1995', 7),
    ('raj_1990', 8),
    ('jane_smith', 7);


-- Insert values into Hashtag table
INSERT INTO Hashtag (hashtag_name, num_posts) 
VALUES 
    ('travel', 5),
    ('art', 8),
    ('coding', 10);

-- Insert values into Has_Hashtag table
INSERT INTO Has_Hashtag (tweet_id, hashtag_name) 
VALUES 
    (1, 'programming'),
    (2, 'technology'),
    (3, 'coding');

-- Insert values into Follows table
INSERT INTO Follows (ufollower, ufollowing) 
VALUES 
    ('jane_smith', 'priya_1985'),
    ('john_doe', 'bob_jones'),
    ('priya_1985', 'jane_smith'),
    ('priya_1985', 'anu_1995');


-- trigger
DELIMITER //
CREATE TRIGGER update_tweet_likes
AFTER INSERT ON Likes_Tweet
FOR EACH ROW
BEGIN
    DECLARE tweet_likes INT;

    -- Get the current number of likes for the tweet
    SELECT num_likes INTO tweet_likes
    FROM tweet
    WHERE tweet_id = NEW.tweet_id;

    -- Update the number of likes in the Tweet table
    UPDATE Tweet
    SET num_likes = tweet_likes + 1
    WHERE tweet_id = NEW.tweet_id;
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_tweet_comments
AFTER INSERT ON comment
FOR EACH ROW
BEGIN
    DECLARE tweet_coms INT;

    -- Get the current number of likes for the tweet
    SELECT num_comments INTO tweet_coms
    FROM tweet
    WHERE tweet_id = NEW.tweet_id;

    -- Update the number of likes in the Tweet table
    UPDATE Tweet
    SET num_comments = tweet_coms + 1
    WHERE tweet_id = NEW.tweet_id;
END;
//
DELIMITER ;
