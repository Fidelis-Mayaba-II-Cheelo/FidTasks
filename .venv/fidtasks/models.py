from itsdangerous import URLSafeTimedSerializer as Serializer
from fidtasks import db, login_manager
from datetime import datetime
from sqlalchemy.orm import backref
from sqlalchemy import Enum
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_image = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    goals = db.relationship('Goal', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.user_image}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id' : self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False, unique=True)
    category = db.Column(Enum('Work', 'Personal', 'Errands'), nullable=False)
    priority = db.Column(Enum('Very High', 'High', 'Medium', 'Low', 'Very Low'), nullable=False)
    status = db.Column(Enum('Pending', 'In-Progress', 'Completed'), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    tasks = db.relationship('Task', backref='goal', lazy=True)

    def __repr__(self):
        return f"Goal('{self.id}', '{self.name}', '{self.description}', '{self.category}''{self.status}','{self.deadline}', '{self.created_at}', '{self.updated_at}', '{self.completed_at}')"

class Task(db.Model):
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), primary_key=True)
    title = db.Column(db.String(20), nullable=False, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    priority = db.Column(Enum('Very High', 'High', 'Medium', 'Low', 'Very Low'), nullable=False)
    status = db.Column(Enum('Pending', 'In-Progress', 'Completed'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Task('{self.goal_id}', '{self.title}', '{self.description}', '{self.priority}''{self.status}', '{self.created_at}', '{self.start_date}', '{self.updated_at}', '{self.deadline}', '{self.completed_at}')"

