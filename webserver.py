from flask import Flask, flash, redirect, url_for, render_template, request, session, send_from_directory, abort, current_app as app
from werkzeug.exceptions import HTTPException
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__, static_folder='static')
app.secret_key = "perezenator"

bannedip = []
@app.before_request
def block_method():
    ip = request.remote_addr
    if ip in bannedip:
        print(f"BLOCKED: {bannedip}")
        abort(403)

@app.errorhandler(HTTPException)
def handle_exception(e):
    if request.remote_addr in bannedip:
        print("yeap")
    else:
        bannedip.append(request.remote_addr)
        print("maybe")
    print(f"nope: {bannedip}")
    return "forbidden", 403

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/sourcecode")
def sc():
    return render_template("sc.html")

@app.route("/ai", methods=["POST", "GET"])
def ai():
    if request.method == "POST":
        msg = request.form["msg"]
        uid = request.remote_addr
        response = requests.get(f"http://api.brainshop.ai/get?bid=163704&key=xBDm1tVuChi8YHpI&uid={uid}&msg={msg}").json()["cnt"]
        print(f"{uid}: {msg}")
        print(f"Charis: {response}")
        return render_template("ai.html", response=response)
    else:
        return render_template("ai.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
