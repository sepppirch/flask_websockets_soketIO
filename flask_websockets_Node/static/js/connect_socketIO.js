
var socket;
var lastval = 0;


$(document).ready(function(){

    ///set up and connect to socket
    console.log('http://' + document.domain + ':' + location.port + '/chat');
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.io.opts.transports = ['websocket'];
    
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    socket.on('status', function(data) {
        //$('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        //$('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('ex', function(data) {
        //console.log("server returned: " + JSON.stringify(data));
        switch(data.fn)
        {
            case 'mkB':
                makeButton(data.id, data.msg, data.msg);
                break;

            case 'scb':
                settextscroll(data.id, data.msg);
                break;
                
            case 'rem_butt_del':
                if ($('#' + data.parent).find('#' + data.id).length) {
                    // found! -> remove in only in that div
                    $('#' + data.parent).find('#' + data.id).remove();
                }
                break;
            case 'sel':
                var select = document.getElementById(data.id).shadowRoot.getElementById("dropdown");
                select.value = data.opt;
                // cold also add options.... select.append(new Option("reeeee"));
                break; 
            
            
        }
        
        
    });

});

