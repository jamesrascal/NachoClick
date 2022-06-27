import os
import json
import string
import secrets
from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
baseURL = 'http://nacho.click/'
nachDB = 'urldb.json'
# wtf flask form to submit generated URL.
class ShortURLForm(FlaskForm):
    userURL = StringField('Enter URL to be shortened', validators=[DataRequired()])

# The main Nach.Click functions
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>',methods=['GET','POST'])
def entry_point(path):
    # Attempts to load the DB fails if it's not on disk.
    try:
        f = open(nachDB)
    except:
        return('Loading of the NachoDB failed')
    nachodata = json.load(f)
    if request.method == 'GET':
        # Checks if there's a path in the URL then redirects.
        if path in nachodata:
            return redirect(nachodata[path], code=302)
        # If no route is found then default to the main template
        return render_template('main.html', form=ShortURLForm())
    if request.method == 'POST':
        # Generates a short URL from user submitted long URL
        shorty = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(8))  # Uses secrets to make the secret
        try:
            nachodata[shorty] = request.form['userURL']  # Save to dict then redirect.
        except:
            return render_template('error.html', message='Something went wrong saving URL (ERROR URLFS01)')
        with open('urldb.json', 'w') as f:
            json.dump(nachodata, f)
        return render_template('url.html', shortURL=f"{baseURL}{shorty}")
    else:
        return render_template('error.html', message='Something went wrong?')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)