from flask import Flask, request
import sys
import bcrypt

sys.path.append('../')
from model import sql_connection, Insert, delete, Show
from pass_generator import generate_password, encrypt, decrypt

app = Flask(__name__)
master_key = None


@app.route('/')
def index():
    if master_key:
        conn = sql_connection()
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed = cur.fetchone()[0]
        if bcrypt.checkpw(master_key.encode(), hashed.encode()):
            return 'Authentication successful!'
        else:
            return """<!DOCTYPE html><html><script>
            var request = new XMLHttpRequest();
            request.open("GET", "reset", false);
            request.send(null);
            </script><body><p>Wrong password, refresh page to try again</p></body></html>""", 403
    else:
        return """<!DOCTYPE html><html><head><script>
        var request = new XMLHttpRequest();
        request.open("GET", "authenticate?password=" + window.prompt("Enter your password"), false);
        request.send(null);
        window.location.reload();
        </script></head></html>"""


@app.route('/authenticate')
def authenticate():
    global master_key
    master_key = request.args.get('password')
    return ''


@app.route('/reset')
def reset():
    global master_key
    master_key = None
    return ''


app.run()
