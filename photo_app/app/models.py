from app import db
from datetime import datetime
from sqlalchemy import Text # Added Text for Album description

# Association table for the many-to-many relationship
# between Photo and Category
photo_categories = db.Table('photo_categories',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

# Association table for the many-to-many relationship
# between Photo and Album
photo_albums = db.Table('photo_albums',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True)
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # The 'photos' backref is added implicitly by the Photo.categories relationship

    def __repr__(self):
        return f'<Category {self.name}>'

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    filepath = db.Column(db.String(512), unique=True, nullable=False) # Path relative to UPLOAD_FOLDER
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    categories = db.relationship('Category', secondary=photo_categories,
                                 lazy='subquery', backref=db.backref('photos', lazy='dynamic'))
    
    albums = db.relationship('Album', secondary=photo_albums,
                             lazy='subquery', backref=db.backref('photos', lazy='dynamic'))

    def __repr__(self):
        return f'<Photo {self.filename}>'

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # The 'photos' backref is added implicitly by the Photo.albums relationship

    def __repr__(self):
        return f'<Album {self.name}>'
