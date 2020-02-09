from flask import Blueprint, render_template, request, session

from post.models import Post, User

general_app = Blueprint('general_app', __name__)

tag_dict = {
    "maths": "maths",
    "compsci" : "cs",
    "chemistry" : "chemistry",
    "biology" : "biology",
    "physics" : "physics",
    "general" : "general"
}

@general_app.route('/')
def index():
    tag = request.args.get('action')
    if tag is None or tag == 'all':
        post = Post.objects()
    else:
        tag_list = [tag_dict.get(tag)]
        post = Post.objects(tags__in=tag_list)

    post = reversed(post)

    if 'username' in session:
        user = User.objects.get(username=session['username'])
        upvote_posts = user.upvote_posts

        return render_template('index.html', post=post, tag=tag, upvote_posts=upvote_posts)
    return render_template('index.html', post=post, tag=tag)