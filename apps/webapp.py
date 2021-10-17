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
            data = Show(master_key, conn)
            # Style credit: w3schools.com
            return_value = """<!DOCTYPE html><html><head><style>
            table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}
            td, th {border: 1px solid #dddddd; text-align: left; padding: 8px;}
            </style></head><body>
            <table><tr><th><b>ID</b></th><th><b>Username</b></th><th><b>Website</b></th><th><b>Password</b</th>"""
            for row in data:
                return_value += '<tr>'
                return_value += f'<th>{str(row[0])}</th>'
                return_value += f'<th>{row[1]}</th>'
                return_value += f'<th>{row[2]}</th>'
                return_value += f'<th>{decrypt(master_key, row[3])}</th>'
                return_value += '</tr>'
            return_value += '</table></body></html>'
            return return_value
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
