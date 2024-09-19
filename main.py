from flask import Flask

from controllr.fantasy_team_controller import teams_blueprint
from controllr.player_controller import players_blueprint
from seed.seed import seed

app = Flask(__name__)

app.register_blueprint(players_blueprint, url_prefix="/api/players")
app.register_blueprint(teams_blueprint, url_prefix="/api/teams")

seed()

if __name__ == '__main__':
    app.run(debug=True)
