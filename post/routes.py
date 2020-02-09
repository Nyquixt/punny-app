from flask import Blueprint, render_template, url_for, redirect, \
    session, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from hashlib import sha256
import os
import json

from utility.decorators import login_required
from post.forms import UploadForm
from post.models import Post

from user.models import User

post_app = Blueprint('post_app', __name__)

@login_required
@post_app.route('/upload', methods=['GET', 'POST'])
def upload():

    if 'username' in session:
        form = UploadForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                # create new record
                new_post = Post()
                new_post.poster = User.objects.get(username=session['username']).id
                new_post.title = form.title.data
                new_post.tags = [x for x in form.tags.data]
                
                if form.link.data:
                    new_post.link = form.link.data
                
                if request.files.get('meme'):
                    filename = secure_filename(form.meme.data.filename)
                    hashed_fname = sha256(filename.encode('utf-8')).hexdigest()
                    file_path = os.path.join('upload_folder', hashed_fname)
                    form.meme.data.save(file_path)
                    new_post.image = hashed_fname
                
                new_post.save()

                return redirect(url_for('general_app.index'))

        return render_template('post/upload.html', form=form)
    else:
        return abort(403)
    

@post_app.route('/image/<id>')
def image(id):
    try:
        post = Post.objects.get(id=id)
    except:
        return abort(404)
    
    fname = post.image
    return send_from_directory('upload_folder', fname)

@login_required
@post_app.route('/upvote', methods=['POST'])
def upvote():
    if 'username' in session:
        if request.method == 'POST':
            data = json.loads(request.data)

            post = Post.objects.get(id=data['postid'])
            user = User.objects.get(username=session['username'])
            
            if post:
                post.update(upsert=True, inc__upvotes_count=1)
                
                upvote_posts = user.upvote_posts
                if post.id not in upvote_posts:
                    # insert new upvoted post (id) to user list
                    upvote_posts.append(post.id)

                # save back to db
                user.upvote_posts = upvote_posts
                user.save()

                return json.dumps({
                    "status" : "success"
                })
            return json.dumps({
                "status" : "no post found"
            })
        return redirect(url_for('general_app.index'))
    else:
        return redirect(url_for('user_app.login'))

@login_required
@post_app.route('/unupvote', methods=['POST'])
def unupvote():
    if 'username' in session:
        if request.method == 'POST':
            data = json.loads(request.data)

            post = Post.objects.get(id=data['postid'])
            user = User.objects.get(username=session['username'])
            
            if post:
                post.update(upsert=True, dec__upvotes_count=1)
                
                upvote_posts = user.upvote_posts

                upvote_posts.remove(post.id)

                # save back to db
                user.upvote_posts = upvote_posts
                user.save()

                return json.dumps({
                    "status" : "success"
                })
            return json.dumps({
                "status" : "no post found"
            })
        return redirect(url_for('general_app.index'))
    else:
        return redirect(url_for('user_app.login'))