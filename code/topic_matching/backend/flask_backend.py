from flask import Flask, jsonify, request
from flask_cors import CORS
from app import load_json, load_users, load_content, match_content, match_without_threshold, get_alternative_suggestions

app = Flask(__name__)
CORS(app)

@app.route('/run_matching', methods=['GET'])
def run_matching():
    users = load_users()
    content = load_content()
    matched_results = match_content(users, content)
    return jsonify(matched_results)

@app.route('/run_new_matching', methods=['POST'])
def run_new_matching():
    user_data = [request.json]
    #print(type(user_data))
    content = load_content()
    #print('user_data', user_data)
    matched_results = match_content(user_data, content)
    #print('matched result', matched_results)
    return jsonify(matched_results)

@app.route('/run_matching_without_threshold', methods=['POST'])
def run_matching_without_threshold():
    user_data = [request.json]
    content = load_content()
    matched_results = match_without_threshold(user_data, content)
    return jsonify(matched_results)

@app.route('/get_suggestions_based_on_type', methods=['POST'])
def get_suggestions_based_on_type():
    user_data = [request.json]
    content = load_content()
    suggestions = get_alternative_suggestions(user_data, content)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
