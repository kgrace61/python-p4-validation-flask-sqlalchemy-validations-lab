from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name: 
            raise ValueError('Author name is required')
        existing_name = Author.query.filter_by(name=name).first()
        if existing_name and existing_name.id != self.id:
            raise ValueError('Author name must be unique')
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and not phone_number.isdigit():
            raise ValueError('Phone number must only contain digits')
        if phone_number and len(phone_number) != 10:
            raise ValueError('Phone number must be exactly 10 digits')
        return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def has_title(self, key, title):
        click_bait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title: 
            raise ValueError('post must have title')
        if not any(keyword in title for keyword in click_bait):
            raise ValueError('Post title must contain clickbait')
        return title
        
    
    @validates('content')
    def is_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters')
        return content
    
    @validates('summary')
    def is_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary must be less than 250 characters')
        return summary

    @validates('category')
    def is_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be Fiction or Non-Fiction')
        return category
    
    

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
