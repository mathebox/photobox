from flask import render_template, copy_current_request_context
from flask import appcontext_tearing_down
from app import app, socketio
import photobox


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
    photobox.send_initial_photo_count()
