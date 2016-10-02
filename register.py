from flask import Flask
from flask import render_template, url_for, redirect, request, flash
from models import Users
from settings import session
from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

app = Flask(__name__)
app.secret_key = '8w9q8DOSHACXNASFZXV'
@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users(name=form.username.data, password=form.password.data)
        session.add(user)
        session.commit()
        session.flush()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)