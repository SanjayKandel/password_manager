from flask import Flask, request
import sys
import bcrypt

sys.path.append('../')
from model import sql_connection, Insert, delete, Show
from pass_generator import generate_password, encrypt, decrypt

app = Flask(__name__)
master_key = None


def get_weaknesses_in_password(password: str):
    result = ''
    if len(password) < 8:
        result += f'\u2022 Password contains {len(password)} characters, a minimum of 8 characters is recommended\n'
    small_letter_found = False
    cap_letter_found = False
    num_found = False
    for letter in password:
        if letter.islower():
            small_letter_found = True
            break
    for letter in password:
        if letter.isupper():
            cap_letter_found = True
            break
    for letter in password:
        if letter.isdigit():
            num_found = True
            break
    if not small_letter_found:
        result += '\u2022Password contains no small letters<br>'
    if not cap_letter_found:
        result += '\u2022Password contains no capital letters<br>'
    if not num_found:
        result += '\u2022Password contains no numbers'
    return result.strip('<br>')


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
            return_value = '<!DOCTYPE html><html><head><style>' \
                           'table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}' \
                           'td, th {border: 1px solid #dddddd; text-align: left; padding: 8px;}' \
                           '</style><script>' \
                           'function add(){' \
                           'var request = new XMLHttpRequest();' \
                           'request.open("GET", "add?website=" + document.getElementById(\'website-input\').value + "&username=" + document.getElementById(\'username-input\').value + "&password=" + document.getElementById(\'password-input\').value, false);' \
                           'request.send(null);' \
                           'if (request.response == ""){' \
                           'window.location.reload();}' \
                           'else {' \
                           'document.getElementById("password error p").innerHTML = request.response;}}' \
                           '</script></head><body>' \
                           '<table><tr>' \
                           '<th><b>ID</b></th><th><b>Username</b></th><th><b>Website</b></th><th><b>Password</b</th>'
            for row in data:
                return_value += '<tr>'
                return_value += f'<th>{str(row[0])}</th>'
                return_value += f'<th>{row[1]}</th>'
                return_value += f'<th>{row[2]}</th>'
                return_value += f'<th>{decrypt(master_key, row[3])}</th>'
                return_value += '</tr>'
            return_value += '</table><input id="website-input"><br>' \
                            '<input id="username-input"><br>' \
                            '<input id="password-input"><br>' \
                            '<button onclick="add()">Add</button>' \
                            '<p id="password error p"></p></body></html>'
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


@app.route('/add')
def add():
    if master_key:
        website = request.args.get('website')
        username = request.args.get('username')
        password = request.args.get('password')
        weaknesses_in_password = get_weaknesses_in_password(password)
        conn = sql_connection()
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        if password:
            if weaknesses_in_password:
                return f'<!DOCTYPE html><html><body><p>Your password has the following weakness:<br>{weaknesses_in_password}</p></body></html>'
            else:
                temp = encrypt(master_key, password.encode())
                items = (username, website, temp)
                Insert(conn, items)  # adding element to db
                return ''
        else:
            password = generate_password()
            temp = encrypt(master_key, password)
            items = (username, website, temp)
            Insert(conn, items)  # adding element to db
            return ''
    else:
        return """<!DOCTYPE html><html><head><script>
        var request = new XMLHttpRequest();
        request.open("GET", "authenticate?password=" + window.prompt("Enter your password"), false);
        request.send(null);
        window.location.reload();
        </script></head></html>"""


app.run()