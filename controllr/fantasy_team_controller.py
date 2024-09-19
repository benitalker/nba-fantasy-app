from flask import Blueprint, request, jsonify
from service.team_service import create_new_team, update_existing_team, remove_team, retrieve_team

teams_blueprint = Blueprint("teams", __name__)

@teams_blueprint.route('/', methods=['POST'])
def create_team_route():
    data = request.json
    team_name = data.get('team_name')
    player_ids = data.get('player_ids')
    try:
        team_id = create_new_team(team_name, player_ids)
        return jsonify({'team_id': team_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@teams_blueprint.route('/<int:team_id>', methods=['PUT'])
def update_team_route(team_id):
    data = request.json
    player_ids = data.get('player_ids')
    try:
        update_existing_team(team_id, player_ids)
        return jsonify({'message': 'Team updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@teams_blueprint.route('/<int:team_id>', methods=['DELETE'])
def delete_team_route(team_id):
    try:
        remove_team(team_id)
        return jsonify({'message': 'Team deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@teams_blueprint.route('/<int:team_id>', methods=['GET'])
def get_team_route(team_id):
    team = retrieve_team(team_id)
    if team:
        return jsonify(team), 200
    else:
        return jsonify({'error': 'Team not found'}), 404
