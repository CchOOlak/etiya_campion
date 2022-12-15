from math import ceil, floor


class Team:

    def __init__(self, name, id, strength) -> None:
        self.id = id
        self.name = name
        self.strength = strength
    
    def present(self):
        return f'Team {self.id + 1} -> name: {self.name} - strength: {self.strength}'

class Scoreboard:

    def __init__(self, teams) -> None:
        self.teams = {}
        self.total_strength = 0
        for id, team in enumerate(teams):
            self.teams[id] = team
            self.total_strength += team.strength
        # [score, team_id]
        self.board = [[0, i] for i in range(len(teams))]
        self.chances = [float(t.strength * 100. / self.total_strength) for t in self.teams.values()]
        self.first_week = True
    
    def get_team(self, id):
        return self.teams.get(id, None)

    def reorder(self):
        self.board = sorted(self.board, lambda x: x[0], reversed=True)

    def get_current_rank(self, team_id):
        for rank, team in enumerate(self.board):
            if team[1] == team_id:
                return rank + 1

    def update(self, team_id, change_score):
        team_index = self.get_current_rank(team_id) - 1
        self.board[team_index][1] += change_score
    
    def chance_of_campion(self):
        chances = []
        if self.first_week:
            return self.chances
        for team_id, chance in enumerate(self.chances):
            rank = self.get_current_rank(team_id)
            rank_prob = float((len(self.board) - rank) * 100. / len(self.board))
            chances.append((rank_prob + chance) / 2.)
        return chances
    
    def predict(self, host_chance, guest_chance):
        host_goals = int(round(host_chance / 10))
        guest_goals = int(round(guest_chance) / 10)

        return (host_goals, guest_goals)



class League:

    def __init__(self, scoreboard) -> None:
        self.scoreboard = scoreboard
        self.fixture = []
        self.report = '\n'.join([t.present() for t in scoreboard.teams.values()])
    
    def arrange(self):
        team_number = len(self.scoreboard.teams.values())
        match_number = team_number * (team_number - 1)
        week_match_number = floor(team_number / 2)
        week_number = ceil(match_number / week_match_number)

        matches = set()
        for src in range(team_number):
            for des in range(team_number):
                if src != des:
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
            self.report += '\n'.join(f'\t\t{self.scoreboard.get_team(t[0]).name} - {self.scoreboard.get_team(t[1]).name}' for t in week)

    def play(self):
        self.report += '\n\n'
        for w, matches in enumerate(self.fixture):
            self.report += f'\n\tchance of campion before week {w + 1}:\n'
            chances = self.scoreboard.chance_of_campion()

            self.report += '\n'.join([f'\t\t{t.name}: %{"%.2f" % chances[t.id]}' for t in self.scoreboard.teams.values()])
            
            self.report += f'\n\tresult of week {w + 1}:\n'
            for match in matches:
                h, g = match[0], match[1]
                h_goal, g_goal = self.scoreboard.predict(chances[h], chances[g])
                self.scoreboard.first_week = False

                self.report += f'\t\t{self.scoreboard.get_team(h).name} {h_goal} - {g_goal} {self.scoreboard.get_team(g).name}\n'
