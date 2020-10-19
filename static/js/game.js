class Game {
    constructor() {
        this.field = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ];
        this.x_win_count = 0;
        this.o_win_count = 0;
        this.draw_count = 0;

        this.game_div = document.getElementById('game');

        this.stat_xwin = document.createElement('p');
        this.stat_owin = document.createElement('p');
        this.stat_draw = document.createElement('p');
        document.body.appendChild(this.stat_xwin);
        document.body.appendChild(this.stat_owin);
        document.body.appendChild(this.stat_draw);
    }

    update_field() {
        this.game_div.innerHTML = '';

        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                var cell = document.createElement('div');
                cell.setAttribute('onclick', 'game.move(' + i + ', ' + j + ')');
                cell.innerText = this.field[i][j];
                this.game_div.appendChild(cell);
            }
        }
    }

    update_stats() {
        this.stat_xwin.innerText = 'X wins: ' + this.x_win_count;
        this.stat_owin.innerText = 'O wins: ' + this.o_win_count;
        this.stat_draw.innerText = 'DRAWS: ' + this.draw_count;
    }

}

class GameServer {
    constructor() {
        this.player_id = /\/([^\/]*)$/.exec(document.URL)[1];
        this.session_id = /\/([^\/]*)\/[^\/]*$/.exec(document.URL)[1];

        this.game = new Game();

        this.ws = new WebSocket('ws://' + document.location.host + '/ws/' + this.session_id + '/' + this.player_id);

        var self = this;
        this.ws.onmessage = function(e) {
            var data = JSON.parse(e.data);
    
            self.game.field = data.game_field;
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
