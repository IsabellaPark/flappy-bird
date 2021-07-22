from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
import matplotlib
import matplotlib.pyplot as plt
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db = SQLAlchemy(app)
app.secret_key = os.getenv('PASSWORD')

class Game(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  gameNumber =db.Column(db.Integer, unique=False, nullable=False)
  score = db.Column(db.Integer, unique=False, nullable=True)

@app.route('/')
def home():
  return render_template('index.html')

#### -- To BE CUSTOMIZED 
@app.route('/stats')
def statistics():
  games = Game.query.all()
  lowest = 1000
  highest = 0
  total = sum = 0

  for game in games:
    print("Game #: " + str(game.gameNumber) + " Score: " + str(game.score))

    if game.score < lowest:
      lowest = game.score
    if game.score > highest:
      highest = game.score

    sum  += game.score
    total += 1

  average = sum/total  

  return render_template('stats.html', low =lowest, high = highest, number = total, avg = round(average,1))

@app.route('/graph')
def graph():
  return render_template('graph.html') 

##--- END FOR "TO BE CUSTOMIZED"

@app.route('/api/<score>/')
def save_score(score):
  
  number = db.session.query(Game).count()
  number += 1
  points = int(score) - 1
  print("Game Number: " + str(number))
  print("Score: " + str(points))
  new_game = Game(gameNumber=number, score = points)
    
  # add the new game to the database
  db.session.add(new_game)
  db.session.commit()

  return redirect("/")

if __name__ == '__main__':
  db.create_all()
  app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host
		port=random.randint(2000, 9000)  # Randomly select the port 
	)