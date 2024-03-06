from flask import Flask, render_template, flash, redirect, url_for
from forms import CreateAccountForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cdeac8f173801449a79cf1c89ab2b757'


names = ['Udbhav',
        'Dhriti',
        'Vasanthi',
        'Balaji',
        'Nyra','dfdfd','fsfsdsdsd','sfgfhfdfsdf']

@app.route('/')
def layout():
    return render_template('layout.html')

@app.route('/home')
def home():
    return render_template('home.html', names=names, title='Home')


@app.route('/test')
def test():
    return render_template('old_templates/testing.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('create_account.html', title="Create Account", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash('You have logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check your username and/or password.', 'danger')
    return render_template('login.html', title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
    