function ws_search_on_message(e) {
    window.location.replace(e.data);
}

var search_label = document.getElementById('search_label');
var seconds = 0;
var minutes = 0;
function display_search_time() {
    seconds += 1;
    if (seconds >= 60) {
        minutes += 1;
        seconds = 0;
    }
    if (minutes <= 0)
    {
        search_label.innerText = ('search: ' + seconds);
    }
    else {
        search_label.innerText = ('search: ' + minutes + ':' + seconds);
    }
}

document.getElementById('search_x').onclick = function(e) {
    var search_ws = new WebSocket(search_ws_base_url + '/X');
    search_ws.onmessage = ws_search_on_message;
    setInterval(display_search_time, 1000);
}

document.getElementById('search_o').onclick = function(e) {
    var search_ws = new WebSocket(search_ws_base_url + '/O');
    search_ws.onmessage = ws_search_on_message;
    setInterval(display_search_time, 1000);
}