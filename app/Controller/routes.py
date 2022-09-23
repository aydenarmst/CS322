from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post, Tag, postTags
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
def likePost(post_id):
    incrementLikes = Post.query.filter_by(id = post_id).first()
    incrementLikes.likes += 1
    db.session.add(incrementLikes)
    db.session.commit()
    return redirect(url_for('routes.index'))





