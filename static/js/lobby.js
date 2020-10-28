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
    var search_ws = new WebSocket(searchX_ws_url);
    search_ws.onmessage = ws_search_on_message;
    setInterval(display_search_time, 1000);
}

document.getElementById('search_o').onclick = function(e) {
    var search_ws = new WebSocket(searchO_ws_url);
    search_ws.onmessage = ws_search_on_message;
    setInterval(display_search_time, 1000);
}




var xhr = new XMLHttpRequest();
xhr.onload = function() {
    var response = JSON.parse(xhr.response);
    document.getElementById('players_now').innerText = response.players_now;
    document.getElementById('players_Xsearch').innerText = response.players_Xsearch;
    document.getElementById('players_Osearch').innerText = response.players_Osearch;
};


function update_statistic() {
    xhr.open('GET', statistic_url);
    xhr.send();
}
setInterval(update_statistic, 1000)
