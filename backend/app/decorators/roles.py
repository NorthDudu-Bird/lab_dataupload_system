from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from ..common.exceptions import AppError
from ..models.user import SysUser


def get_current_user():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    user = SysUser.query.get(int(user_id)) if user_id else None
    if not user:
        raise AppError("用户不存在或登录状态失效", 401, 401)
    if user.status != "enabled":
        raise AppError("账号已被禁用，请联系管理员", 403, 403)
    return user


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if roles and user.role not in roles:
                raise AppError("无权访问该资源", 403, 403)
            return func(*args, **kwargs)

        return wrapper

    return decorator

