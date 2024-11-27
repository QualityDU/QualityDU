import enum
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class UserRole(enum.Enum):
    admin = 1
    user = 2
    export = 3


class User(db.Model, UserMixin):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    created_tags = db.relationship("Tag", back_populates="creator")
    assigned_tags = db.relationship("ActTag", back_populates="assigner")

    def __repr__(self):
        return f"<User {self.username}>"

    def get_id(self):
        return str(self.user_id)


class Act(db.Model):
    __tablename__ = "acts"

    act_id = db.Column(db.Integer, primary_key=True)
    du_code = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    journal_no = db.Column(db.Integer, nullable=False, default=0)
    num_edits = db.Column(db.Integer, nullable=False, default=0)
    text_payload = db.Column(db.Text, nullable=False)
    date_scraped = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    last_edited_date = db.Column(db.Date, nullable=True)
    last_tag_added_date = db.Column(db.Date, nullable=True)
    position = db.Column(db.Integer, nullable=False, default=0)  
    part_no = db.Column(db.Integer, nullable=False, default=0)  
    
    tags = db.relationship("ActTag", back_populates="act")

    def __repr__(self):
        return f"<Act {self.du_code}>"


class Tag(db.Model):
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    num_assigned = db.Column(db.Integer, nullable=False, default=0)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='SET NULL'))
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    last_assigned_date = db.Column(db.Date)

    creator = db.relationship("User", back_populates="created_tags")
    acts = db.relationship("ActTag", back_populates="tag")


    def __repr__(self):
        return f"<Tag {self.name}>"
    

class ActTag(db.Model):
    __tablename__ = "acts_tags"

    id = db.Column(db.Integer, primary_key=True)
    act_id = db.Column(db.Integer, db.ForeignKey('acts.act_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False, default=date.today)
    assigner_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='SET NULL'))

    act = db.relationship("Act", back_populates="tags")
    tag = db.relationship("Tag", back_populates="acts")
    assigner = db.relationship("User", back_populates="assigned_tags")

    def __repr__(self):
        return f"<ActTag {self.id}: Act {self.act_id} - Tag {self.tag_id}>"
