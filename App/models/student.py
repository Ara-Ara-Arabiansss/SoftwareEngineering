from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    total_points = db.Column(db.Integer, nullable = False)
    overall_rank = db.relationship("Ranking", uselist=False, backref='student', lazy=True)
    notification = db.relationship("Notification", backref='student', lazy=True)
    competitions = db.relationship("StudentCompetition", lazy=True, backref=db.backref("competitions"), cascade="all, delete-orphan")

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
            # 'competitions': self.competitions
        }
    
    def participate_in_competition(self):
        return 0


