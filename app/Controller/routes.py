from __future__ import print_function
from pprint import pformat
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import login_required, current_user

from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm, SortForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET','POST'])
@login_required
def index():
    pform = SortForm()
    posts = Post.query.order_by(Post.timestamp.desc())
    if pform.is_submitted():
        if (pform.sort.data == '1'):
            posts = Post.query.order_by(Post.timestamp.desc())
        elif (pform.sort.data == '2'):
            posts = Post.query.order_by(Post.title.desc())
        elif (pform.sort.data == '3'):
            posts = Post.query.order_by(Post.happiness_level.desc())
        elif (pform.sort.data == '4'):
            posts = Post.query.order_by(Post.likes.desc())
    else:
        posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title='Smile Portal',postCount = posts.count(),posts = posts.all(), form = pform)


@bp_routes.route('/postsmile/', methods=['GET', 'POST'])
@login_required
def postsmile():
    pform = PostForm()
    if pform.validate_on_submit():
        newPost = Post(title = pform.title.data, body = pform.body.data, happiness_level = pform.happiness_level.data, tags = pform.tag.data)
        allTags = Tag.query.all()
        for t in allTags:
            if t in pform.tag.data:
                newPost.tags.append(t)
        db.session.add(newPost)
        db.session.commit()
        flash("Title " + newPost.title + " is created")
        return redirect(url_for('routes.index'))
    return render_template('create.html', form=pform)


@bp_routes.route('/like/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    incrementLikes = Post.query.filter_by(id = post_id).first()
    incrementLikes.likes += 1
    db.session.add(incrementLikes)
    db.session.commit()
    return redirect(url_for('routes.index'))





