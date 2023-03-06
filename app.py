from boggle import Boggle
from flask import Flask, redirect, session, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "hey"
app.debug = True
# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

toolbar = DebugToolbarExtension(app)
# This is a bit of hack, but don't use Flask DebugToolbar
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

boggle_game = Boggle()

@app.route("/")
def home():
    """Shows board and allows for a guess"""

    board = boggle_game.make_board()
    session['board'] = board
    hs = session.get("hs", 0)
    num_plays = session.get("num_plays", 0)
    return render_template("index.html", board = board, hs=hs, num_plays=num_plays)

@app.route("/check")
def check():
    """Checks if word is valid"""

    word = request.args["word"]
    board = session["board"]
    resp = boggle_game.check_valid_word(board, word)
    json = jsonify({"res": resp})
    return json

@app.route("/final-score", methods=["POST"])
def final_score():
    score = request.json["score"]
    hs = session.get("hs",0)
    num_plays = session.get("num_plays", 0)

    session["num_plays"] = num_plays +1
    session["hs"] = max(score, hs)

    return jsonify(record = score > hs)



