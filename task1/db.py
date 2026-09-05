from flask import Flask, request, redirect, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import DeclarativeBase 
from sqlalchemy.orm import Mapped, mapped_column 

import secrets
import string

import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("db_password")
#Creates the base class that SQLAlchemy uses to build all database tables.
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


#Define a table named user
class URL(db.Model):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] 
    short_code: Mapped[str] = mapped_column(unique=True)


# create the app instance
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/url_shortener"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# initialize the app with the extension
db.init_app(app)


with app.app_context():
    db.create_all() 


#short code generation 
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


@app.get("/")
def home():
    return render_template("index.html")

#Create route to get and give url 
@app.post("/shorten")
def shorten_url():
  original_url = request.form.get("original_url")

  if not original_url:
      return jsonify({"error": "original_url is required"}), 400

  # Generate a unique short code
  while True:
      code = generate_short_code()

      existing = db.session.execute(
          db.select(URL).where(URL.short_code == code)
      ).scalar_one_or_none()

      if existing is None:
          break
    
  #Saving python obj
  url = URL(
    original_url = request.form["original_url"],
    short_code = code,
  )
  
  db.session.add(url)
  db.session.commit()

  return jsonify(
        {
            "original_url": original_url,
            "short_url": request.host_url + code,
        }
    )


@app.get("/<string:short_code>")
def redirect_url(short_code):
    url = db.session.execute(
        db.select(URL).where(URL.short_code == short_code)
    ).scalar_one_or_none()

    if url is None:
        return jsonify({"error": "Short URL not found"}), 404

    return redirect(url.original_url)


if __name__ == "__main__":
    app.run(debug=True)




