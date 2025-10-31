from flask import jsonify


def api_response(code=None, message="", data=None):
    """统一API返回格式"""
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    }), code if code else 200
