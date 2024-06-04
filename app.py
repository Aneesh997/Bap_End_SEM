from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Song
from forms import SongForm, SearchForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('index.html', songs=songs)

@app.route('/add', methods=['GET', 'POST'])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(
            title=form.title.data,
            artist=form.artist.data,
            album=form.album.data
        )
        db.session.add(new_song)
        db.session.commit()
        flash('Song added successfully!')
        return redirect(url_for('index'))
    return render_template('add_song.html', form=form)

@app.route('/delete/<int:song_id>')
def delete_song(song_id):
    song = Song.query.get(song_id)
    if song:
        db.session.delete(song)
        db.session.commit()
        flash('Song deleted successfully!')
    else:
        flash('Song not found.')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    songs = []
    if form.validate_on_submit():
        search_term = form.search_term.data
        songs = Song.query.filter(
            Song.title.contains(search_term) | 
            Song.artist.contains(search_term) | 
            Song.album.contains(search_term)
        ).all()
    return render_template('search.html', form=form, songs=songs)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
