from flask import render_template, flash, redirect, url_for, request
from songsavvy.models import User, Search
from songsavvy.forms import CreateAccountForm, LoginForm, UpdateAccountForm, SearchForm
from songsavvy import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from songsavvy.spotify_client import SpotifyClient, get_id_from_url
import json


app.app_context().push()

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created. Please log in!', 'success')
        return redirect(url_for('login'))
    return render_template('create_account.html', title="Create Account", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check your username and/or password.', 'danger')

    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    form = UpdateAccountForm()
    return render_template('account.html', title='My Account', form=form)
    
@app.route('/input', methods=['GET', 'POST'])
def input():
    form = SearchForm()
    if form.validate_on_submit():
        # Add code to connect to spotify api to get track features
        pass
    return render_template('input.html', title='Enter Track URL', form=form)

@app.route('/results', methods=['GET'])
def result():
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id
    client = SpotifyClient()
    song_url = request.args.get('song_url')
    song_id = get_id_from_url(song_url)
    track = client.get_tracks(song_id)
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    j = json.dumps(track, indent=4)
    with open('response.json', 'w') as fp:
        json.dump(j, fp)
    print(user_id)
    search = Search(
        track_url=song_url,
        track_name=track_name, 
        artist=artist_name,
        user_id=user_id
        )
    db.session.add(search)
    db.session.commit()
    return render_template('result.html', title='Result', track=track)