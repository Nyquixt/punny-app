from app import db

class User(db.Document):
    # db_field nickname for attribute
    username = db.StringField(db_field="username", required=True, unique=True)
    password = db.StringField(db_field="password", required=True)
    upvote_posts = db.ListField(db_field='upvote_posts')