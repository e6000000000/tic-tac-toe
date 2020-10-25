function ws_search_on_message(e) {
    window.location.replace(e.data);
}

document.getElementById('search_x').onclick = function(e) {
    var search_ws = new WebSocket(search_ws_base_url + '/X');
    search_ws.onmessage = ws_search_on_message;
}

document.getElementById('search_o').onclick = function(e) {
    var search_ws = new WebSocket(search_ws_base_url + '/O');
    search_ws.onmessage = ws_search_on_message;
}