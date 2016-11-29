
from flask import Flask, render_template
import zmq

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<int:pl>")
def player(pl):
    return render_template("player.html", player=pl)

@app.route("/<path:pl>/<path:b>")
def playerCommand(pl, b):
    try:
        ctx = zmq.Context()
        sock = ctx.socket(zmq.REQ)
        sock.bind('tcp://*:8888')
        print("Player %s -> %s" % (pl,b))
        sock.send_string("%s_%s" % (pl, b))
        response = sock.recv()
        return response
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
