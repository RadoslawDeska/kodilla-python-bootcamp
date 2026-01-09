from flask import Blueprint, abort, current_app, jsonify, request

from app.auth import api_admin_required, get_serializer

from .model import RoleEnum, User

users_bp = Blueprint("users", __name__, url_prefix="/api/v2/users")


# Allow registering single admin for empty database
@users_bp.route("/bootstrap-admin", methods=["POST"])
def bootstrap_admin():
    # Prevent api route guessing by setting secret header
    secret = request.headers.get("X-Bootstrap-Secret")
    if secret != current_app.config.get("ADMIN_SECRET_KEY"):
        abort(403)

    # Check if database has `admin` user
    if User.query.filter_by(role="admin").first():
        return jsonify({"error": "Admin already exists"}), 403

    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        abort(400)

    # Set admin
    try:
        new_admin = User(
            email=data["email"], password=data["password"], role=RoleEnum.admin
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_admin.create()
    return jsonify(
        {
            "message": f"Bootstrap admin {new_admin.email} created",
            "role": new_admin.role.value,
        }
    ), 201


@users_bp.route("/login", methods=["POST"])
def api_login():  # everyone can log in after registration through WEB interface
    data = request.get_json()
    if not data:
        abort(400)

    user = User.get_by_email(data.get("email"))
    if not user or not user.check_password(data.get("password")):
        abort(403)

    # ADMIN-ONLY ACCESS
    # if user.role.value != "admin":
    #     abort(403)

    s = get_serializer(current_app)  # Keep the user as hashed token for safety
    token = s.dumps({"user_id": user.id, "role": user.role.value})

    return jsonify({"access_token": token, "token_type": "Bearer"})


@users_bp.route("/register", methods=["POST"])
@api_admin_required  # Only admin can register new users through API
def register_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        abort(400)

    # Check if email exists
    if User.get_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 409

    try:
        new_user = User(
            email=data["email"],
            password=data["password"],
            role=data.get("role", "user"),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_user.create()
    return jsonify(
        {
            "message": f"User {new_user.email} registered",
            "role": new_user.role.value,
        }
    ), 201
