from flask import Flask
from src.utils import generate_fake_teams
from src.model import Scoreboard, League

app = Flask(__name__)


@app.route('/fixture/<team_number>', methods=['POST'])
def fixture(team_number):

    teams = generate_fake_teams(int(team_number))
    scoreboard = Scoreboard(teams)
    league = League(scoreboard)
    league.arrange()
    league.play()

    return league.report
