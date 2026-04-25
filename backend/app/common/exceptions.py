from flask import current_app
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from .response import fail
from ..extensions import db


class AppError(Exception):
    def __init__(self, message="业务处理失败", code=400, http_status=400, data=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.http_status = http_status
        self.data = data


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return fail(error.message, error.code, error.data, error.http_status)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return fail("参数校验失败", 422, error.messages, 422)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        current_app.logger.exception(error)
        return fail("数据已被引用或唯一字段重复，请检查后重试", 409, http_status=409)

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return fail(error.description, error.code, http_status=error.code)

    @app.errorhandler(Exception)
    def handle_unknown_error(error):
        db.session.rollback()
        current_app.logger.exception(error)
        return fail("服务器内部错误", 500, http_status=500)

    _register_jwt_handlers(app.extensions["flask-jwt-extended"])


def _register_jwt_handlers(jwt: JWTManager):
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return fail("请先登录", 401, {"reason": reason}, 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return fail("登录状态无效", 401, {"reason": reason}, 401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return fail("登录已过期，请重新登录", 401, http_status=401)

