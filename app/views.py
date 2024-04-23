from flask import render_template
from app import app, socketio
from . import photobox


@app.route('/')
@app.route('/index')
def index():
    photobox.start()
    return render_template('index.html')


@app.route('/button')
def capture_button():
    photobox.start()
    return render_template('index.html', show_button=True)


@socketio.on('capture', namespace='/test')
def capture_image():
    photobox.capture_photo()


@socketio.on('connect', namespace='/test')
def test_connect():
    started = photobox.start()
    if not started:
        photobox.send_initial_photo_count()
