from flask import Flask, redirect, url_for, render_template, request, abort, current_app as app
from werkzeug.exceptions import HTTPException
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

@app.errorhandler(404)
def handle_exception(error):
    if request.remote_addr in bannedip:
        print("404 banned")
    else:
        bannedip.append(request.remote_addr)
        print("banned")
    return "forbidden", 403

@app.errorhandler(505)
def handle_exception(error):
    if request.remote_addr in bannedip:
        print("505 banned")
    else:
        bannedip.append(request.remote_addr)
        print("banned")
    return "forbidden", 403

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route("/")
def home():
    return redirect(url_for('ai'))

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
    app.run(host='0.0.0.0', port=5000, debug=False)