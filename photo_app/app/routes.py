import os
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Category, Photo, Album # Added Album
import os

# Use ALLOWED_EXTENSIONS from app.config
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # --- POST Request Logic ---
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Check if a photo with the same filename already exists
            existing_photo = Photo.query.filter_by(filename=filename).first()
            if existing_photo:
                flash(f'A photo with the name "{filename}" already exists. Please rename your file or upload a different one.', 'error')
                return redirect(request.url)

            file.save(filepath)
            
            # Create Photo object
            new_photo = Photo(filename=filename, filepath=filepath)
            
            # Process selected categories
            selected_category_ids = request.form.getlist('categories')
            for cat_id in selected_category_ids:
                category = Category.query.get(cat_id)
                if category:
                    new_photo.categories.append(category)
            
            db.session.add(new_photo)
            db.session.commit()
            
            flash('File uploaded successfully and saved to database with categories!')
            return redirect(url_for('gallery'))
        else:
            flash('File type not allowed.')
            return redirect(request.url)
    # --- GET Request Logic ---
    categories = Category.query.all()
    return render_template('upload.html', categories=categories)

@app.route('/gallery')
def gallery():
    category_id = request.args.get('category_id', type=int)
    all_categories = Category.query.all()
    current_category_name = None
    
    if category_id:
        category = Category.query.get(category_id)
        if category:
            photos = category.photos.all() # Or Photo.query.filter(Photo.categories.any(id=category_id)).all()
            current_category_name = category.name
        else:
            photos = [] # Or flash a message "Category not found" and show all photos
            flash(f'Category with ID {category_id} not found.', 'error')
            # Optionally, redirect to the main gallery or show all photos
            # photos = Photo.query.order_by(Photo.uploaded_at.desc()).all()
    else:
        photos = Photo.query.order_by(Photo.uploaded_at.desc()).all()

    # The 'images' variable in the template expects filenames, not Photo objects.
    # We need to adjust the template or pass Photo objects and access photo.filename there.
    # For now, let's stick to passing Photo objects as it's cleaner.
    
    return render_template('gallery.html', 
                           photos=photos, 
                           all_categories=all_categories, 
                           current_category_name=current_category_name)

@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/add_album', methods=['GET', 'POST'])
def add_album():
    if request.method == 'POST':
        album_name = request.form.get('album_name')
        album_description = request.form.get('album_description')

        if not album_name:
            flash('Album name cannot be empty.', 'error')
        else:
            existing_album = Album.query.filter_by(name=album_name).first()
            if existing_album:
                flash(f'Album "{album_name}" already exists.', 'error')
            else:
                new_album = Album(name=album_name, description=album_description)
                db.session.add(new_album)
                db.session.commit()
                flash(f'Album "{album_name}" created successfully.', 'success')
                return redirect(url_for('add_album')) # Redirect to clear form / show updated list
    
    albums = Album.query.order_by(Album.created_at.desc()).all()
    return render_template('add_album.html', albums=albums)

@app.route('/album/<int:album_id>/manage', methods=['GET', 'POST'])
def manage_album_contents(album_id):
    album = Album.query.get_or_404(album_id) # Fetches album or returns 404 if not found

    if request.method == 'POST':
        photo_ids = request.form.getlist('photo_ids')
        photos_added_count = 0
        for photo_id in photo_ids:
            photo = Photo.query.get(photo_id)
            if photo:
                if photo not in album.photos: # Check if photo is not already in the album
                    album.photos.append(photo)
                    photos_added_count += 1
        if photos_added_count > 0:
            db.session.commit()
            flash(f'{photos_added_count} photo(s) added to album "{album.name}".', 'success')
        else:
            flash('No new photos were selected or added.', 'info')
        return redirect(url_for('manage_album_contents', album_id=album_id))

    # GET request
    all_photos = Photo.query.order_by(Photo.uploaded_at.desc()).all()
    return render_template('manage_album_contents.html', album=album, all_photos=all_photos)

@app.route('/albums', methods=['GET'])
def list_albums():
    albums = Album.query.order_by(Album.name).all()
    return render_template('albums_list.html', albums=albums)

@app.route('/album/<int:album_id>', methods=['GET'])
def view_album(album_id):
    album = Album.query.get_or_404(album_id)
    # The relationship 'photos' on Album model is lazy='dynamic' by default from backref,
    # so album.photos is a query builder. Call .all() or similar to get actual photos.
    # If lazy='subquery' or 'joined' was used on Photo.albums, then album.photos would be a list.
    # Given the model definition: Photo.albums -> backref=db.backref('photos', lazy='dynamic')
    # So, album.photos needs to be queried.
    photos = album.photos.order_by(Photo.uploaded_at.desc()).all()
    return render_template('view_album.html', album=album, photos=photos)

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if category_name:
            existing_category = Category.query.filter_by(name=category_name).first()
            if existing_category:
                flash(f'Category "{category_name}" already exists.', 'error')
            else:
                new_category = Category(name=category_name)
                db.session.add(new_category)
                db.session.commit()
                flash(f'Category "{category_name}" added successfully.', 'success')
                return redirect(url_for('add_category'))
        else:
            flash('Category name cannot be empty.', 'error')
    categories = Category.query.all()
    return render_template('add_category.html', categories=categories)
