import json

class Statistic:
    players_now = 0
    players_Xsearch = 0
    players_Osearch = 0

    @staticmethod
    def as_json():
        jsn = {
            'players_now': Statistic.players_now,
            'players_Xsearch': Statistic.players_Xsearch,
            'players_Osearch': Statistic.players_Osearch,
        }
        return json.dumps(jsn)