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
    
class Dialogue(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid1()))
    session_id = db.Column(db.String(36), db.ForeignKey("session.id"))
    text = db.Column(db.Text(), nullable=True) # Text overall
    is_human = db.Column(db.Boolean, default=False)
    current_seg = db.Column(db.Integer, nullable=True, default=0)
    max_seg = db.Column(db.Integer, nullable=True, default=0) # Add an additional thread to check if current_seg is equal to max_seg
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self):
        return f"Dialogue>>> {self.id}"
    
class Segments(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid1()))
    dialogue_id = db.Column(db.String(36), db.ForeignKey("dialogue.id"))
    text = db.Column(db.Text(), nullable=True)
    video_ready = db.Column(db.Boolean, default=False)
    idx = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self):
        return f"Segments>>> {self.id}"
    

