document.addEventListener("DOMContentLoaded", function(event) {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('photo', function(msg) {
        var photo = document.getElementById('photo');
        var photo_count = document.getElementById('photo-count');
        var fallback_text = document.querySelector('p.fallback-text');
        if ('message' in msg) {
            photo_count.textContent = '';
            fallback_text.textContent = msg.message;
            photo.style.display = 'none';
        } else {
            photo.setAttribute('src', msg.photo_path + "?" + new Date().getTime());
            photo_count.textContent = msg.photo_count;
            fallback_text.textContent = 'Start taking photos';
            photo.style.display = 'block';
        }
    });
    document.getElementById('capture-button').addEventListener('click', function (e) {
        socket.emit('capture');
        return false;
    });
});
