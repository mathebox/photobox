from flask import render_template, copy_current_request_context
from flask import appcontext_tearing_down
from app import app, socketio
import subprocess
import threading
import time


thread = None
photo_count = 0
default_image_path = 'static/img/pic.jpg'


def start_background_thread():
    global thread
    if thread is None:
        thread = threading.Thread(target=count_photos)
        thread.daemon = True
        thread.start()


def current_photo_count():
    ls_proc = subprocess.Popen(['ls', 'fakecam'], stdout=subprocess.PIPE)
    return len(list(ls_proc.stdout))


def download_latest_photo(photo_nr):
    default_image_path_app = 'app/%s' % default_image_path
    if photo_nr == 0:
        rm_proc = subprocess.Popen(['rm', default_image_path_app],
                                   stdout=subprocess.PIPE)
        return
    ls_proc = subprocess.Popen(['ls', '-t', 'fakecam'],
                               stdout=subprocess.PIPE)
    file_name = list(ls_proc.stdout)[0].strip()
    new_image_path = 'fakecam/%s' % file_name
    cp_proc = subprocess.Popen(['cp', new_image_path, default_image_path_app],
                               stdout=subprocess.PIPE)
    cp_proc.wait()


def send_latest_photo(photo_count, broadcast=True):
    socketio.emit('photo', {
        'photo_count': photo_count,
        'photo_path': default_image_path,
    }, broadcast=broadcast, namespace='/test')


def count_photos():
    global photo_count
    photo_count = current_photo_count()
    download_latest_photo(photo_count)
    send_latest_photo(photo_count)
    while True:
        time.sleep(0.5)
        new_photo_count = current_photo_count()
        if new_photo_count != photo_count:
            photo_count = new_photo_count
            download_latest_photo(photo_count)
            send_latest_photo(photo_count)


@app.route('/')
@app.route('/index')
def index():
    start_background_thread()
    return render_template('index.html')


@app.route('/button')
def capture_button():
    start_background_thread()
    return render_template('index.html', show_button=True)


@socketio.on('capture', namespace='/test')
def capture_image():
    snapshot_path_old = 'snapshot.jpg'
    snapshot_path_new = 'fakecam/snapshot-%d.jpg'
    image_proc = subprocess.Popen(['imagesnap', '-q'], stdout=subprocess.PIPE)
    image_proc.wait()
    mv_proc = subprocess.Popen(['mv',
                                snapshot_path_old,
                                snapshot_path_new % photo_count],
                               stdout=subprocess.PIPE)


@socketio.on('connect', namespace='/test')
def test_connect():
    send_latest_photo(photo_count, broadcast=False)
