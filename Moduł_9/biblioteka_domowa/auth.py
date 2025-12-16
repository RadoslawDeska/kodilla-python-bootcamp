from functools import wraps

from flask import abort, redirect, session, url_for, request, current_app
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


def get_serializer(app):
    return URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="api-auth")


def web_login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "web_user_id" not in session:  # session expired, redirect
            return redirect(url_for("home"))
        return fn(*args, **kwargs)

    return wrapper


# auth.py
def api_login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            abort(401)
        token = auth.removeprefix("Bearer ").strip()
        s = get_serializer(current_app)
        try:
            data = s.loads(token, max_age=3600)  # 1h
        except (SignatureExpired, BadSignature):
            abort(401)
        request.api_user_id = data.get("user_id")
        request.api_user_role = data.get("role")
        return fn(*args, **kwargs)

    return wrapper


def api_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            abort(401)

        token = auth.removeprefix("Bearer ").strip()
        s = get_serializer(current_app)

        try:
            data = s.loads(token, max_age=3600)  # 1h
        except SignatureExpired:
            abort(401)
        except BadSignature:
            abort(401)

        if data.get("role") != "admin":
            abort(403)

        request.api_user_id = data["user_id"]
        return fn(*args, **kwargs)

    return wrapper
