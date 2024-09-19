from flask import Blueprint, jsonify, request
from repository.player_repository import get_players_by_position_and_season

players_blueprint = Blueprint("players", __name__)

@players_blueprint.route("/", methods=['GET'])
def get_players_by_position():
    position = request.args.get('position')
    season = request.args.get('season', default=None, type=int)
    if not position or position not in ['C', 'PF', 'SF', 'SG', 'PG']:
        return jsonify({"error": "Position is required and must be one of C, PF, SF, SG, PG."}), 400
    try:
        players = get_players_by_position_and_season(position, season)
        return jsonify(players), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
