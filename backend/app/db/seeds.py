from sqlalchemy import create_engine
from sqlalchemy.sql import text

import random
import string
import os

#find database connection URL
DATABASE_URL = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")

engine = create_engine(DATABASE_URL, echo=False)

user_insert_statement = text("""INSERT INTO users(username, email, salt, bio, hashed_password)
                            VALUES(:username, :email, :salt, :bio, :hashed_password)
                            """)
select_last_user_id = text("""SELECT * FROM users ORDER BY id DESC LIMIT 1""")
select_last_item_id = text("""SELECT * FROM items ORDER BY id DESC LIMIT 1""")
item_statement = text("""INSERT INTO items(slug, title, description, seller_id) 
                    VALUES(:slug, :title, :description, :seller_id)
                    """)
comment_statement = text("""
            INSERT INTO comments (body, seller_id, item_id) 
            VALUES (:body, :seller_id, :item_id)
            """)

letters = string.ascii_lowercase

def create_user_and_item(con, slug):
    username_length = random.randint(10,15)
    random_username = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(username_length))

    user = {
        'username': random_username,
        'email': f'{random_username}@mail.com',
        'salt': 'abc',
        'bio': 'bio',
        'hashed_password': '12345689',
    }

    con.execute(user_insert_statement, **user)

    user_id_result = con.execute(select_last_user_id)

    generated_user_id = None
    for row in user_id_result:
        generated_user_id = row['id']

    item = {
        'slug': slug,
        'title': 'title',
        'description': ' description',
        'seller_id': generated_user_id
     }

    con.execute(item_statement, **item)

    item_id_result = con.execute(select_last_item_id)

    generated_item_id = None
    for row in item_id_result:
        generated_item_id = row['id']

    comment = {
        'body' : ''.join(random.choice(string.printable) for i in range(40)),
        'seller_id' : generated_user_id,
        'item_id' : generated_item_id,
    }

    con.execute(comment_statement, **comment)



with engine.connect() as con:
    for i in range(100):
        create_user_and_item(con, "test item " + str(i))