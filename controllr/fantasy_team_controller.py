from flask import Blueprint, request, jsonify
from service.team_service import create_new_team, update_existing_team, remove_team, retrieve_team, compare_teams, \
    compare_teams_by_name

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

@teams_blueprint.route('/compare', methods=['GET'])
def compare_teams_endpoint():
    team_ids = [request.args.get(f'team{i}') for i in range(1, len(request.args) + 1)]
    team_ids = [team_id for team_id in team_ids if team_id]

    if len(team_ids) < 2:
        return jsonify({"error": "At least two teams must be provided for comparison."}), 400

    try:
        team_ids = list(map(int, team_ids))
    except ValueError:
        return jsonify({"error": "Team IDs must be valid integers."}), 400

    result = compare_teams(team_ids)

    if result is None:
        return jsonify({"error": "One or more teams do not exist."}), 404

    return jsonify(result)

@teams_blueprint.route('/stats', methods=['GET'])
def compare_teams_by_name_endpoint():
    team_names = [request.args.get(f'team{i}') for i in range(1, 4)]
    team_names = [team_name for team_name in team_names if team_name]

    if len(team_names) < 2:
        return jsonify({"error": "At least two teams must be provided for comparison."}), 400
    if len(team_names) > 3:
        return jsonify({"error": "No more than three teams can be compared."}), 400

    result = compare_teams_by_name(team_names)

    if result is None:
        print(result)
        return jsonify({"error": "One or more teams do not exist."}), 404

    return jsonify(result), 200
