# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses
# a background thread
if async_mode == 'eventlet':
    import eventlet  # noqa: F811
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey  # noqa: F811
    monkey.patch_all()


from flask import Flask  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


DEFAULT_IMAGE_PATH = 'static/img/pic.jpg'
