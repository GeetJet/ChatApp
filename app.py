#import sys, os

import slbot
from flask import Flask, render_template, request
from flaskwebgui import FlaskUI

app = Flask(__name__)
app.static_folder = 'static'
#ui = FlaskUI(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if not userText:
        try:
            userText = slbot.listen()
        except:
            return 'sorry, can you say that again or type'
    return str(slbot.qna_response(userText))

if __name__ == "__main__":
    app.run()
    #ui.run()