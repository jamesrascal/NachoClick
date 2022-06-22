import string
import secrets
from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import json
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


class MyForm(FlaskForm):
    userURL = StringField('Enter URL to be shortened', validators=[DataRequired()])

def makeSecret():
    alphabet = string.ascii_letters + string.digits
    thisSecret = ''.join(secrets.choice(alphabet) for i in range(8))
    return thisSecret
def loadnachodata():
    # Opening JSON file
    f = open('urldb.json')
    nachodata = json.load(f)
    return nachodata
@app.route('/')
def entry_point():
    print(request.remote_addr)
    form = MyForm()
    return render_template('main.html', thisSecret=makeSecret(), form=form)

# Displays after creating url
@app.route('/surl', methods=['POST'])
def makeShort():
    print(request.remote_addr)
    nachodata = loadnachodata()
    shorty = makeSecret() # Uses secrets to make the secret
    nachodata[shorty]=request.form['userURL'] # Save to dict then redirect.
    with open('urldb.json', 'w') as f:
        json.dump(nachodata, f)
    return render_template('url.html', shortURL=f"http://nacho.click/l/{shorty}")

# Redirection route
@app.route('/l/<goURL>')
def gotoURL(goURL):
    nachodata = loadnachodata()
    print(goURL)
    if goURL in nachodata:
        return redirect(nachodata[goURL], code=302)
    else:
        return redirect('/', code=302)

@app.route('/account')
def account():
    print('This is the account page')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
