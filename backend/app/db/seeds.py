import random
import sqlalchemy

from faker import Faker
from app.core.config import get_app_settings
from sqlalchemy.sql import text
from app.models.domain.users import UserInDB
from app.models.domain.items import Item
from app.models.domain.comments import Comment

fake = Faker()

SETTINGS = get_app_settings()
DATABASE_URL = SETTINGS.database_url

engine = sqlalchemy.create_engine(DATABASE_URL)

with engine.connect as connection:
    for i in range(100):
        test_username = "Test_User_{i}"
        test_email = fake.email()
        test_password = fake.password()
        test_bio = fake.paragraph()
        test_image = fake.image_url()
        test_user = UserInDB(username=test_username, email=test_email, bio=test_bio, image=test_image)

        connection.execute(
            text(f"""
            INSERT INTO users (username, salt, email, bio, image)
            VALUES ('{test_user.username}', '', '{test_user.email}', '{test_user.bio}', '{test_user.image}')
            """)
        )

        HASHED_PASSWORD = 'test12345'
        connection.execute(
            text(f"UPDATE user SET salt = 'test', hashed_password = '{HASHED_PASSWORD}'")
        )

        test_slug = fake.slug()
        test_title = fake.sentance()
        test_description = fake.description()
        test_tags = [fake.word() for _ in range(3)]
        test_item_image = fake.image_url()
        test_body = fake.text()
        test_item = Item(slug=test_slug, description=test_description, tags=test_tags, seller=test_user,
                         favorited=fake.boolean(), favorites_count=random.randint(0, 100), image=test_item_image,
                         body=test_body)
        connection.execute(
            text(f"""
            INSERT INTO items (slug, title, description, seller_id, image, body)
            VALUES ('{test_item.slug}', '{test_item.title}', '{test_item.description}',
            {i}, '{test_item.image}', '{test_item.body}') 
            """)
        )

        test_comment_body = fake.text()
        test_comment = Comment(body=test_comment_body, seller=test_user)
        connection.execute(
            text(f"""
                    INSERT INTO comments (body, seller_id, item_id) 
                    VALUES ('{test_comment.body}', {i}, {i})
                    """)
        )
