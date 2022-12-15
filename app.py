from flask import Flask
from src.utils import generate_fake_teams
from src.model import Scoreboard, League

app = Flask(__name__)


@app.route('/fixture/<team_number>', methods=['POST'])
def fixture(team_number):

    generate_fake_teams(int(team_number))
    scoreboard = Scoreboard(int(team_number))
    league = League(scoreboard)

    return league.report
