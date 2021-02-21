from flask import Flask, redirect, url_for, render_template, request
from twitter import main


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        main(user)  # loc_map leave main(user)
        return render_template("login.html")
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
