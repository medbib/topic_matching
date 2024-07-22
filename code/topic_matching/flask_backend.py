from flask import Flask, jsonify
from flask_cors import CORS
from app import load_users, load_content, match_content

app = Flask(__name__)
CORS(app)

@app.route('/run_matching', methods=['GET'])
def run_matching():
    users = load_users()
    content = load_content()
    matched_results = match_content(users, content)
    return jsonify(matched_results)

if __name__ == '__main__':
    app.run(debug=True)
