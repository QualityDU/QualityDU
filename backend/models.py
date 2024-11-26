import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class UserRole(enum.Enum):
    admin = 1
    user = 2
    export = 3


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Act(db.Model):
    __tablename__ = "acts"

    act_id = db.Column(db.Integer, primary_key=True)
    du_code = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    journal_no = db.Column(db.Integer, nullable=False, default=0)
    num_edits = db.Column(db.Integer, nullable=False, default=0)
    text_payload = db.Column(db.Text, nullable=False)
    date_scraped = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    last_edited_date = db.Column(db.Date, nullable=True)
    last_tag_added_date = db.Column(db.Date, nullable=True)
    position = db.Column(db.Integer, nullable=False, default=0)  
    part_no = db.Column(db.Integer, nullable=False, default=0)  

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)


class ActTag(db.Model):
    __tablename__ = "acts_tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    act_id = db.Column(db.Integer, db.ForeignKey("acts.act_id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    assigner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    act = db.relationship("Act", backref=db.backref("tags", cascade="all, delete-orphan"))
    assigner = db.relationship("User", backref=db.backref("assigned_tags", lazy="dynamic"))