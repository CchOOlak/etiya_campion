import random
import string
from src.model import Team

def generate_fake_teams(team_number):
    result = []
    s = string.ascii_lowercase
    for i in range(team_number):
        length = ((random.randrange(1, 20) + i) % 13) + 2
        team_name = ''.join(random.choice(s) for i in range(length))
        team_id = i
        team_strength = random.randrange(1, 100)

        team_obj = Team(
            id=team_id,
            name=team_name,
            strength=team_strength
        )
        result.append(team_obj)
    return result
