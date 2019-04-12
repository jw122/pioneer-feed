import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost:5432/pioneer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Update, Goal, Comment


@app.route("/")
def hello():
    all_updates = Update.query.order_by(Update.likes.desc()).all()
    return render_template("home.html", updates=all_updates)

@app.route("/featured")
def get_featured():
    featured = Update.query.filter(Update.likes >= 20).all()
    return render_template("featured.html", updates=featured)

@app.route("/add/form", methods = ['GET', 'POST'])
def create_update():
    if request.method == "POST":
        name=request.form.get('name')
        message=request.form.get('message')
        try:
            update=Update(
                name=name,
                message=message
            )
            db.session.add(update)
            db.session.commit()
            add_msg = "{}'s update was added! Id: {}".format(update.name, update.id)
            return redirect(url_for('hello'))
        except Exception as e:
            return(str(e))

    return render_template("add_update.html")

@app.route("/add")
def add_update():
    name=request.args.get('name')
    message=request.args.get('message')

    try:
        update=Update(
            name=name,
            message=message
        )
        db.session.add(update)
        db.session.commit()
        return "Update added. Update id={}".format(update.id)
    except Exception as e:
	    return(str(e))

@app.route("/get/<name_>")
def get_by_name(name_):
    try:
        updates_set = Update.query.filter_by(name=name_).all()
        goal = Goal.query.filter_by(name=name_).first()
        all_comments = {} # map of update_id -> comments
        for u in updates_set:
            comments = get_comments(u.id)
            all_comments[u.id] = comments
        # print "all comments: ", all_comments
        return render_template("detail.html", person=name_, goal=goal, updates=updates_set, comments=all_comments)
    except Exception as e:
        return(str(e))

@app.route("/upvote/<id_>")
def upvote(id_):
    u = Update.query.filter_by(id=id_).first()
    Update.query.filter_by(id=id_).update({ Update.likes: u.likes + 1})
    db.session.commit()
    return redirect(url_for('hello'))

@app.route("/superlike/<id_>")
def superlike(id_):
    u = Update.query.filter_by(id=id_).first()
    if not u.superlikes:
        u.superlikes = 0
    Update.query.filter_by(id=id_).update({ Update.superlikes: u.superlikes + 1})
    db.session.commit()
    return redirect(url_for('hello'))

@app.route("/comment", methods = ['GET', 'POST'])
def comment():
    author = request.form.get('author')
    comment = request.form.get('comment')
    update_id = request.form.get('update_id')

    try:
        comment = Comment(
            author = author,
            comment = comment,
            update_id = update_id
        )
        db.session.add(comment)
        db.session.commit()
        return ('', 204)

    except Exception as e:
        return(str(e))

# Get comments by update id
@app.route("/get_comments/<id_>")
def get_comments(id_):
    comments = Comment.query.filter_by(update_id=id_).all()
    comments_list = []
    for c in comments:
        comments_list.append((c.author, c.comment))

    return comments_list

if __name__ == '__main__':
    app.run()