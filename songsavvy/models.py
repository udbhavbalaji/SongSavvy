from songsavvy import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    searches = db.relationship('Search', backref='searched_by', lazy=True) 
    
    def __repr__(self):
        return f"User({self.first_name}, {self.last_name}, {self.email}, {self.username})"
    

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_url = db.Column(db.String(120), nullable=False)
    track_name = db.Column(db.String(60), nullable=False)
    artist = db.Column(db.String(60), nullable=False)
    search_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Search({self.track_name}, {self.track_url}, {self.artist})"


class OAuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(200), nullable=False)
    time_accessed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'AccessToken({self.access_token}, {self.time_accessed})'
