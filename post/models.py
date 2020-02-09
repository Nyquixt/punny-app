from app import db
from user.models import User

class Post(db.Document):
    poster = db.ReferenceField(User, db_field='poster')
    upvotes_count = db.IntField(db_field='upvote_count', default=0)
    image = db.StringField(db_field='image')
    title = db.StringField(db_field='title', max_length=100)
    tags = db.ListField(db_field='tags')
    link = db.StringField(db_field='link')
