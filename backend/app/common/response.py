from flask import jsonify


def success(data=None, message="success", code=200, http_status=200):
    return jsonify({"code": code, "message": message, "data": data}), http_status


def fail(message="error", code=400, data=None, http_status=400):
    return jsonify({"code": code, "message": message, "data": data}), http_status

