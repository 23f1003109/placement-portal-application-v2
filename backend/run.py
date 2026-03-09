from flask import jsonify, redirect, url_for
from .app import create_app

app = create_app()

@app.errorhandler(404)
def bad_request(error):
    return jsonify({'error': 'Not Found'}), 404

@app.route('/')
def index():
    return redirect(url_for("auth.login"))

if __name__ == '__main__':
    app.run(debug=True)
