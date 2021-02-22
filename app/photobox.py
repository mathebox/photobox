from app import socketio, DEFAULT_IMAGE_PATH
import threading
import time
from . import dslr as camera


thread = None
photo_count = 0
camera_is_capturing = False


def start():
    global thread
    if thread is None:
        thread = threading.Thread(target=count_photos)
        thread.daemon = True
        thread.start()
        return True
    return False


def count_photos():
    global photo_count
    camera.init()
    photo_count = camera.current_photo_count()
    camera.download_latest_photo(photo_count)
    send_latest_photo(photo_count)
    resend_photo = False
    while True:
        new_photo_count = camera.current_photo_count()
        if new_photo_count < 0 and not camera_is_capturing:
            send_error('Camera not found')
            camera.init()
            resend_photo = True
            time.sleep(0.5)
        elif new_photo_count != photo_count and new_photo_count >= 0:
            photo_count = new_photo_count
            resend_photo = False
            t1 = time.time()
            camera.download_latest_photo(photo_count)
            t2 = time.time()
            send_latest_photo(photo_count)
            t3 = time.time()
            print('download:', (t2-t1), ' ---- send:', (t3-t2))
        elif resend_photo:
            resend_photo = False
            send_latest_photo(photo_count)
        else:
            time.sleep(0.5)


def send_latest_photo(photo_count, broadcast=True):
    socketio.emit('photo', {
        'photo_count': photo_count,
        'photo_path': DEFAULT_IMAGE_PATH,
    }, broadcast=broadcast, namespace='/test')


def send_error(message, broadcast=True):
    socketio.emit('photo', {
        'photo_count': photo_count,
        'message': message,
    }, broadcast=broadcast, namespace='/test')


def send_initial_photo_count():
    send_latest_photo(photo_count, broadcast=False)


def capture_photo():
    global camera_is_capturing
    camera_is_capturing = True
    camera.capture_photo()
    camera_is_capturing = False
