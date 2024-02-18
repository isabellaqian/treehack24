from flask import request, jsonify
from flask import Blueprint
from flask_cors import cross_origin
from flask import send_from_directory

video_stream_blueprint = Blueprint("video_stream", __name__, url_prefix="/api/video_stream")

@video_stream_blueprint.route("/video", methods=["POST", "OPTIONS"])
@cross_origin(origin='*')  # Allows all origins
def video():
    return send_from_directory("/root/MakeItTalk/examples", "anne_pred_fls_hack_test_audio_embed.mp4")

@video_stream_blueprint.route("/hello", methods=["GET"])
def hello_world():
    return "hello world!!"