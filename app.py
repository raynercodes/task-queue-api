from flask import Flask, request
from routes.task_routes import tasks_bp
from routes.auth_routes import auth_bp
from utils.responses import error_response
import os

app = Flask(__name__)

app.register_blueprint(tasks_bp)
app.register_blueprint(auth_bp)

@app.errorhandler(ValueError)
def handle_value_error(e):
    return error_response(str(e), status=400)

@app.errorhandler(Exception)
def handle_internal_error(e):
    return error_response(str(e), status=500)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=5000, debug=True)