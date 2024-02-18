from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
from sqlalchemy.dialects.mysql import MEDIUMBLOB
import uuid

db = SQLAlchemy()

class Session(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid1()))
    company = db.Column(db.String(50), default="Amazon")
    job_description = db.Column(db.Text, default="Tech Company's Job")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self):
        return f"Session>>> {self.company}"
    
class Question(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid1()))
    session_id = db.Column(db.String(36), db.ForeignKey("session.id"))
    text = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self):
        return f"Question>>> {self.text}"
    
class Dialogue(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid1()))
    question_id = db.Column(db.String(36), db.ForeignKey("question.id"))
    text = db.Column(db.Text(), nullable=True) # Text overall
    is_human = db.Column(db.Boolean, default=False)
    max_seg = db.Column(db.Integer, nullable=True, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self):
        return f"Dialogue>>> {self.id}"
    
class Segments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dialogue_id = db.Column(db.String(36), db.ForeignKey("dialogue.id"))
    text = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self):
        return f"Segments>>> {self.id}"
    

