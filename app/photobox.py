from app import socketio, DEFAULT_IMAGE_PATH
import threading
import time
import isight as camera


thread = None
photo_count = 0


def start():
    global thread
    if thread is None:
        thread = threading.Thread(target=count_photos)
        thread.daemon = True
        thread.start()


def count_photos():
    global photo_count
    camera.init()
    photo_count = camera.current_photo_count()
    camera.download_latest_photo(photo_count)
    send_latest_photo(photo_count)
    while True:
        time.sleep(0.5)
        new_photo_count = camera.current_photo_count()
        if new_photo_count != photo_count:
            photo_count = new_photo_count
            camera.download_latest_photo(photo_count)
            send_latest_photo(photo_count)


def send_latest_photo(photo_count, broadcast=True):
    socketio.emit('photo', {
        'photo_count': photo_count,
        'photo_path': DEFAULT_IMAGE_PATH,
    }, broadcast=broadcast, namespace='/test')


def send_initial_photo_count():
    send_latest_photo(photo_count, broadcast=False)


def capture_photo():
    camera.capture_photo()