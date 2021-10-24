from flask import Flask, request
import sys
import bcrypt

sys.path.append('../')
from model import sql_connection, Insert, delete as Delete, Show, update as Update
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
                           'request.open("GET", "add?website=" + encodeURIComponent(document.getElementById(\'website-input\').value) + "&username=" + encodeURIComponent(document.getElementById(\'username-input\').value) + "&password=" + encodeURIComponent(document.getElementById(\'password-input\').value), false);' \
                           'request.send(null);' \
                           'if (request.response == ""){' \
                           'window.location.reload();}' \
                           'else {' \
                           'document.getElementById("password error p").innerHTML = request.response;}}' \
                           """function logout() {
                            var request = new XMLHttpRequest();
                            request.open("GET", "reset", false);
                            request.send(null);
                            window.location.reload();
                            }""" \
                           '</script></head><body><button onclick="logout()">Logout</button><br>' \
                           '<table><tr>' \
                           '<th><b>ID</b></th><th><b>Username</b></th><th><b>Website</b></th><th><b>Password</b</th>'
            for row in data:
                return_value += '<tr>'
                return_value += f'<th>{str(row[0])}</th>'
                return_value += f'<th>{row[1]}</th>'
                return_value += f'<th>{row[2]}</th>'
                return_value += f'<th>{decrypt(master_key, row[3])}</th>'
                return_value += f'<th><button onclick=\'window.location.href = "delete?id={str(row[0])}"\'>Delete' \
                                f'</button></th>'
                return_value += '<th><input id="new password" type="password"></th>'
                return_value += f'<th><button onclick=\'window.location.href = "update?id={str(row[0])}&password=" + document.getElementById("new password").value;\'>Update password</button></th>'
                return_value += '</tr>'
            return_value += '</table><p>Website</p><input id="website-input"><br>' \
                            '<p>Username</p><input id="username-input"><br>' \
                            '<p>Password</p><input id="password-input" type="password"><br>' \
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
        function login() {
        var request = new XMLHttpRequest();
        request.open("GET", "authenticate?password=" + encodeURIComponent(document.getElementById("master password").value), false);
        request.send(null);
        window.location.reload();
        }
        </script></head><body><p>Master password</p><input type="password" id="master password"><br>
        <button onclick="login()">Login</button></body></html>"""


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
        request.open("GET", "authenticate?password=" + encodeURIComponent(document.getElementById("master password").value), false);
        request.send(null);
        window.location.reload();
        </script></head></html>"""


@app.route('/delete')
def delete():
    id_ = int(request.args.get('id'))
    conn = sql_connection()
    cur = conn.cursor()
    cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
    Delete(master_key, conn, id_)
    return '<!DOCTYPE html><html><head><script>window.location.href = "/"</script></head></html>'


@app.route('/update')
def update():
    id_ = int(request.args.get('id'))
    new_password = request.args.get('password')
    conn = sql_connection()
    cur = conn.cursor()
    cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
    weaknesses_in_password = get_weaknesses_in_password(new_password)
    if new_password:
        if weaknesses_in_password:
            return f'<!DOCTYPE html><html><body><p>Your password has the following weakness:<br>{weaknesses_in_password}</p></body></html>'
        else:
            Update(master_key, conn, id_, new_password.encode())
            return '<!DOCTYPE html><html><head><script>window.location.href = "/";</script></head></html>'
    else:
        new_password = generate_password()
        Update(master_key, conn, id_, new_password)
        return '<!DOCTYPE html><html><head><script>window.location.href = "/";</script></head></html>'


app.run()
