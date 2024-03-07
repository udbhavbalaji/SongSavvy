from songsavvy import db
from datetime import datetime


class User(db.Model):
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Search({self.track_name}, {self.track_url}, {self.artist})"

