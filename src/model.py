from math import ceil, floor

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
    
    def arrange(self):
        team_number = len(map_id)
        match_number = (team_number * (team_number - 1)) / 2
        week_match_number = floor(team_number / 2)
        week_number = ceil(match_number / week_match_number)

        matches = set()
        for src in range(team_number):
            for des in range(src + 1, team_number):
                matches.add((src, des))
        
        added_matches = 0
        for w in range(week_number):
            week_matches = []
            week_teams = set()

            while len(week_matches) < week_match_number and added_matches < match_number:
                approval_match = []
                for match in matches:
                    if (match[0] not in week_teams) and (match[1] not in week_teams):
                        approval_match = match
                        break
                week_matches.append(approval_match)
                week_teams.add(approval_match[0])
                week_teams.add(approval_match[1])
                matches.remove(approval_match)
                added_matches += 1
            
            self.fixture.append(week_matches)
        
        self.report += '\n\nFixture plan:\n'
        for ind, week in enumerate(self.fixture):
            self.report += f'\n\tWeek {ind + 1}:\n'
            self.report += '\n'.join(f'\t\t{get_team(t[0]).name} - {get_team(t[1]).name}' for t in week)

