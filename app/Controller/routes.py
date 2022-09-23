from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post
from app.Controller.forms import PostForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="Smile Portal", postCount = posts.count(), posts=posts.all())


@bp_routes.route('/postsmile/', methods=['GET', 'POST'])
def postsmile():
    pform = PostForm()
    if pform.validate_on_submit():
        newPost = Post(title = pform.title.data, body = pform.body.data, happiness_level = pform.happiness_level.data)
        db.session.add(newPost)
        db.session.commit()
        flash("Title " + newPost.title + " is created")
        return redirect(url_for('routes.index'))
    return render_template('create.html', form=pform)


@bp_routes.route('/like/<post_id>', methods=['POST'])
def likePost(post_id):
    incrementLikes = Post.query.filter_by(id = post_id).first()
    incrementLikes.likes += 1
    db.session.add(incrementLikes)
    db.session.commit()
    return redirect(url_for('routes.index'))


@bp_routes.route('/tag/<tag_id>', methods=['POST'])
def tagPost(tag_id):
    tagPost = Post.query.filter_by(id = tag_id).first()
    tagPost.tags.append(tag_id)
    db.session.add(tagPost)
    db.session.commit()
    return redirect(url_for('routes.index'))


@bp_routes.route('/postTags/<post_id>', methods=['GET'])
def postTags(post_id):
    post = Post.query.filter_by(id = post_id).first()
    return render_template('postTags.html', post=post)