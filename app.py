from flask import Flask, send_file
from flask_cors import CORS
from video_stream import video_stream_blueprint
from database.database import db

app = Flask(__name__)

CORS(app, support_credentials=True, resources={r"/api/*": {"origins": "*"}})  # Enable CORS globally

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.secret_key = "randomkey_kwfqwc_qwef!"
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
app.config["SESSION_COOKIE_NAME"] = "session"
app.config["SESSION_COOKIE_SECURE"] = True

app.register_blueprint(video_stream_blueprint)

db.init_app(app)

@app.route("/")
def home():
    # Example: Return a simple message
    return "Welcome to the Flask App!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
