from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'{self.name} - {self.description}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref=db.backref("posts", lazy=True))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/categories")
def categories():
    all_categories = Category.query.all()
    return render_template('categories.html', categories=all_categories)

@app.route("/category/add", methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category = Category(
            name = request.form['name'],
            description = request.form['description']
        )
        db.session.add(category)
        db.session.commit()
    return render_template("add_category.html")

@app.route("/post/add", methods=['GET', 'POST'])
def add_post():
    all_categories = Category.query.all()
    if request.method == 'POST':
        post = Post(
            title = request.form['title'],
            content = request.form['content'],
            author = request.form['author'],
            category_id = int(request.form['category_id'])
        )
        db.session.add(post)
        db.session.commit()
    return render_template("add_post.html", categories=all_categories)

@app.route("/posts")
def posts():
    all_posts = Post.query.all()
    return render_template("posts.html", posts=all_posts)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
