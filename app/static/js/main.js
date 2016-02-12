$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('photo', function(msg) {
        var $photo = $('#photo')
        $photo.attr('src', msg.photo_path + "?" + new Date().getTime());
        $photo.show();
        $('#photo-count').text(msg.photo_count);
    });
    $('#capture-button').click(function(event) {
        socket.emit('capture');
        return false;
    });
});
