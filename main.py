from flask import Flask, render_template, g, request, flash
import sqlite3
import os
from FDataBase import FDataBase

DATABASE = '/tmp/flsite.bd'
DEBUG = True
SECRET_KEY = 'jscid.c84f84hf,j23fcwniwec9e>?kde'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

def connect_db():
   conn = sqlite3.connect(app.config['DATABASE'])
   conn.row_factory = sqlite3.Row
   return conn

def create_db():
   db = connect_db()
   with app.open_resource('sq_db.sql', mode='r') as f:
      db.cursor().executescript(f.read())
   db.commit()
   db.close()
   
def get_db():
   if not hasattr(g, 'link_db'):
      g.link_db = connect_db()
   return g.link_db

@app.teardown_appcontext
def close_db(error):
   if hasattr(g, 'link_db'):
      g.link_db.close()

@app.route("/")
def index():
   return render_template("main.html")

@app.route("/resume")
def resume():
   return render_template("resume.html")

@app.route("/reviews", methods=["POST", "GET"])
def reviews():
   db = get_db()
   dbase = FDataBase(db)
   if request.method == "POST":
      res = dbase.addComment(request.form["username"], request.form["email"], request.form["comment"])
      if not res:
         flash("Ошибка добавления комментария", category = 'error')
      else:
         flash("Комментарий добавлен успешно", category = 'success')
   return render_template('reviews.html', comments=dbase.getComments())


if __name__ == "__main__":
   app.run(debug=True)