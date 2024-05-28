CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash bytea,
    password_salt bytea
);


CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    user_id INT,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
            REFERENCES users(user_id)
            ON DELETE CASCADE
);


INSERT INTO users (username, email, password_hash, password_salt) VALUES ('admin', 'admin@gmail.com', 'admin', 'admin');

INSERT INTO posts (user_id, title, content, created_at) VALUES (1, 'firstpost', 'a lot of text', '2016-06-22 19:10:25-07');