map_id = {}


class Team:

    def __init__(self, name, id, strength) -> None:
        self.id = id
        self.name = name
        self.strength = strength

    def persist(self):
        map_id[self.id] = self
    
    def present(self):
        return f'Team {self.id} -> name: {self.name} - strength: {self.strength}'


def get_team(id):
    return map_id.get(id, None)


class Scoreboard:

    def __init__(self, team_number) -> None:
        # [score, team_id]
        self.board = [[0, i] for i in range(team_number)]

    def reorder(self):
        self.board = sorted(self.board, lambda x: x[0], reversed=True)

    def get_current_rank(self, team_id):
        for rank, team in enumerate(self.board):
            if team[1] == team_id:
                return rank + 1

    def update(self, team_id, match_result):
        # lose result
        change_value = 0
        if match_result == 1:
            # tie result
            change_value += 1
        if match_result == 2:
            # win result
            change_value += 2
        team_index = self.get_current_rank(team_id) - 1
        self.board[team_index][1] += change_value


class League:

    def __init__(self, scoreboard) -> None:
        self.scoreboard = scoreboard
        self.week = 1
        self.fixture = []
        self.report = '\n'.join([t.present() + '\n' for t in map_id.values()])
    
    # def arrange(self):
    #     team_number = len(map_id)
    #     match_number = (team_number * (team_number - 1)) / 2
    #     week_match_number = team_number / 2
    #     week_number = match_number / week_match_number

    #     for team in range(map_id.values()):
    #         for 
