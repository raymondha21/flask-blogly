"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.Text,
                     nullable=False,
                     unique=True)

    last_name = db.Column(db.Text,
                     nullable=False,
                     unique=True,
                     default = "")
    
    image_url = db.Column(db.Text,
                     nullable=False, 
                     default="https://i.stack.imgur.com/l60Hf.png")

    posts = db.relationship("Posts", backref="user", cascade="all, delete-orphan")
                     
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

class Posts(db.Model):
    """Posts model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text,
                     nullable=False)

    content= db.Column(db.Text,
                     nullable=False)
    
    created_at = db.Column(
                db.DateTime,
                nullable=False,
                default=datetime.datetime.now)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Tags(db.Model):
    """Tags Model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.Text,
                     nullable=False,    
                     unique=True)

    posts = db.relationship('Posts'
                            ,secondary="post_tag"
                            ,backref="tags")

class PostTag(db.Model):
    """Maps posts with tags"""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
                    db.ForeignKey("posts.id"),
                    primary_key=True)

    tags_id = db.Column(db.Integer,
                    db.ForeignKey("tags.id"),    
                    primary_key=True)
          

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
