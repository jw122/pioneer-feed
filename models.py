from app import db
from datetime import datetime

class Update(db.Model):
    __tablename__ = 'updates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    message = db.Column(db.String())
    time = db.Column(db.String())
    likes = db.Column(db.Integer)
    superlikes = db.Column(db.Integer)

    def __init__(self, name, message):
        self.name = name
        self.message = message
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.likes = 0
        self.superlikes = 0
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'message': self.message,
            'time': self.time,
            'likes': self.likes,
            'superlikes': self.superlikes
        }

class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    goal = db.Column(db.String())

    def __init__(self, name, message):
        self.name = name
        self.goal = goal
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'goal': self.goal
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer(), primary_key=True)
    update_id = db.Column(db.Integer())
    author = db.Column(db.String())
    comment = db.Column(db.String())

    def __init__(self, update_id, author, comment):
        self.update_id = update_id
        self.author = author
        self.comment = comment
    
    def serialize(self):
        return {
            'id': self.id,
            'update_id': self.update_id,
            'author': self.author,
            'comment': self.comment
        }
