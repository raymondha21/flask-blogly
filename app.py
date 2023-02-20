"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Posts, Tags

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'thebestsecretkey'


connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Homepage redirects to list of users."""

    return redirect("/users")


@app.route('/users')
def users():
    """List of users page"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/users.html', users=users)


@app.route('/users/new')
def users_new_form():
    """Form for a new user"""

    return render_template('new_user.html')


@app.route('/users/new', methods=["POST"])
def users_new():
    """Handles post request with information from form"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_page(user_id):
    """See profile of specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Edit profile page"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_edit_handle(user_id):
    """Handles edit request"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url'] or None

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete')
def users_delete(user_id):
    """Delete User"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def users_posts_form(user_id):
    """Render new post form"""

    user = User.query.get_or_404(user_id)

    return render_template('posts/new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def users_posts_new(user_id):
    """Handles new post request"""

    new_post = Posts(
        title=request.form['title'],
        content=request.form['content'],
        user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_page(post_id):
    """Renders post page"""

    post = Posts.query.get_or_404(post_id)

    return render_template('posts/post_page.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit_form(post_id):
    """Edit post page"""

    post = Posts.query.get_or_404(post_id)

    return render_template('posts/post_edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_edit(post_id):
    """Edit post page"""

    post = Posts.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    if(request.form['tag']):
        new_tag = Tags(name = request.form['tag'])
        post.tags.append(new_tag)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete')
def post_delete(post_id):
    """Handles post delete"""

    post = Posts.query.get_or_404(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/tags')
def tags():
    """List of tags page"""

    tags = Tags.query.order_by(Tags.name).all()
    return render_template('tags/tags.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """New tags page"""

    return render_template('tags/new_tags.html')


@app.route('/tags/new', methods=["POST"])
def tags_new():
    """Handles new tag request"""

    new_tag = Tags(
        name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tags_id>')
def tags_page(tags_id):
    """Tags details page"""

    tag = Tags.query.get_or_404(tags_id)
    posts = tag.posts

    return render_template("tags/tags_detail.html", tag=tag, posts=posts)


@app.route('/tags/<int:tags_id>/edit')
def tags_edit_form(tags_id):
    """Tags edit form"""

    tag = Tags.query.get_or_404(tags_id)

    return render_template("tags/tags_edit.html", tag=tag)


@app.route('/tags/<int:tags_id>/edit', methods=["POST"])
def tags_edit(tags_id):
    """Handles tag edit request"""

    tag = Tags.query.get_or_404(tags_id)

    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tags_id>/delete')
def tags_delete(tags_id):
    """Handles tags deletion request"""

    tag = Tags.query.get_or_404(tags_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
