$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('photo', function(msg) {
        var $photo = $('#photo');
        var $photo_count = $('#photo-count');
        var $fallback_text = $('p.fallback-text');
        if ('message' in msg) {
            console.log('error');
            $photo_count.text('');
            $fallback_text.text(msg.message);
            $photo.hide();
        } else {
            console.log('show');
            $photo.attr('src', msg.photo_path + "?" + new Date().getTime());
            $photo.show();
            $photo_count.text(msg.photo_count);
            $fallback_text.text('Start taking photos');
        }
    });
    $('#capture-button').click(function(event) {
        socket.emit('capture');
        return false;
    });
});
