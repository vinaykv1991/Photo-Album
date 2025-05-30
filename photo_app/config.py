import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
