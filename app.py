from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
app.app_context().push()

# Models for todo
class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"
    
# Home Page
@app.route('/', methods = ['GET','POST'])
def home():
   if request.method == 'POST':
       title = (request.form['title'])
       desc = (request.form['desc'])
       todo = ToDo(title = title, desc = desc)
       db.session.add(todo)
       db.session.commit()
   allTodo = ToDo.query.all()
   return render_template("index.html", allTodo = allTodo)

# About Page
@app.route('/about')
def about():
    return render_template("about.html")

# Show Page
@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        todoUpdate = ToDo.query.filter_by(sno=sno).first()
        todoUpdate.title = title
        todoUpdate.desc = desc
        db.session.add(todoUpdate)
        db.session.commit()
        return redirect("/")
    todo_update = ToDo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo_update = todo_update)

# Show Page
@app.route('/delete/<int:sno>')
def delete(sno):
    todo_delete = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo_delete)
    db.session.commit()
    return redirect("/")

# @app.route('/products')
# def products():
#     return 'This is akash offcial page'

if __name__ == "__main__":
    app.run(debug = True, port = 8000)