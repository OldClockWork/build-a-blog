from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Champ12345@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#----------------------POST CONFIRMATION
@app.route("/postCon", methods=["POST"])
def posting():
    
    title = request.form['title']
    body = request.form['body']
    error = ""

    if(title.strip() == "" or body.strip() == ""):
        error = "Error: Title or textarea can't not be left empty..."
        return render_template("newpost.html", error=error)

    else:
        post = Blog(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return render_template("postCon.html")


#----------------------CREATE POST
@app.route("/newpost", methods=["GET"])
def new_post():
    return render_template("newpost.html")


#----------------------FOCUS ON CLICKED POST
@app.route("/focus_post", methods=["GET"])
def post_focus():
    id = request.args.get("id")  
    entry = Blog.query.get(int(id))
    return render_template("focus_post.html", title=entry.title, body=entry.body)


#----------------------MAIN PAGE
@app.route("/", methods=['POST', 'GET'])
def index():
    post = Blog.query.filter_by().all()
    return render_template("main.html", blog = post)


if __name__ == '__main__':
    app.run()