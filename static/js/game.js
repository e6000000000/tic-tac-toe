class Game {
    constructor() {
        this.field = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ];
        this.restart_votes = 0;
        this.x_win_count = 0;
        this.o_win_count = 0;
        this.draw_count = 0;

        this.game_div = document.getElementById('game');
        this.stats_div = document.getElementById('stats');

        this.restart_btn = document.getElementById('restart');
        this.stat_xwin = document.createElement('p');
        this.stat_owin = document.createElement('p');
        this.stat_draw = document.createElement('p');
        this.stats_div.appendChild(this.stat_xwin);
        this.stats_div.appendChild(this.stat_owin);
        this.stats_div.appendChild(this.stat_draw);
    }

    update_field() {
        this.game_div.innerHTML = '';

        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                var cell = document.createElement('div');
                cell.setAttribute('class', 'cell');
                cell.setAttribute('onclick', 'game.move(' + j + ', ' + i + ')'); //should be redesigned
                cell.innerText = this.field[i][j];
                this.game_div.appendChild(cell);
            }
        }
    }

    update_stats() {
        this.restart_btn.innerText = 'restart (' + this.restart_votes + ')'; 
        this.stat_xwin.innerText = 'X wins: ' + this.x_win_count;
        this.stat_owin.innerText = 'O wins: ' + this.o_win_count;
        this.stat_draw.innerText = 'Draws: ' + this.draw_count;
    }

}

class GameServer {
    constructor() {
        this.player_id = /\/([^\/]*)$/.exec(document.URL)[1];
        this.session_id = /\/([^\/]*)\/[^\/]*$/.exec(document.URL)[1];

        this.game = new Game();

        this.ws = new WebSocket(websocket_url);

        var self = this;
        this.ws.onmessage = function(e) {
            var data = JSON.parse(e.data);
    
            self.game.field = data.game_field;
            self.game.restart_votes = data.restart_votes;
            self.game.x_win_count = data.x_win_count;
            self.game.o_win_count = data.o_win_count;
            self.game.draw_count = data.draw_count;
            self.game.update_field();
            self.game.update_stats();
        }
    }

    move(x, y) {
        var jsn = {
            command: 'move',
            x: x,
            y: y
        };
        this.ws.send(JSON.stringify(jsn));
    }

    restart() {
        var jsn = {
            command: 'restart'
        };
        this.ws.send(JSON.stringify(jsn));
    }
}

var game = new GameServer();
document.getElementById('restart').onclick = ()=> game.restart();
document.getElementById('lobby').onclick = function() {
    window.location.replace(host + '/game');
}
document.getElementById('friend_url').onclick = function() {
    try {
        navigator.clipboard.writeText(friend_url);
    } catch (error) {
        alert('cant copy to clipboard');
    }
}
