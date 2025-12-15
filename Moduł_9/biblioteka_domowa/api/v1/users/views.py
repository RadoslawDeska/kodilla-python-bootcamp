from flask import Blueprint, jsonify, abort, request, session, current_app

from .model import User

from .model import RoleEnum

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

@users_bp.before_request
def require_admin():
    # wyjątki dla login i logout
    if request.endpoint in ("users.bootstrap_admin", "users.api_login", "users.api_logout"):
        return  # Allow to log in or log out

    is_admin = session.get("logged_in") and session.get("role") == "admin"
    if not is_admin:
        abort(403)

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
            email=data["email"],
            password=data["password"],
            role=RoleEnum.admin
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_admin.create()
    return jsonify({
        "message": f"Bootstrap admin {new_admin.email} created",
        "role": new_admin.role.value
    }), 201

@users_bp.route("/login", methods=["POST"])
def api_login():
    data = request.get_json()
    if not data:
        abort(400)

    email = data.get("email")
    password = data.get("password")

    user = User.get_by_email(email)
    if user and user.check_password(password):
        if user.role.value != "admin":
            return jsonify({"error": "Only admin can log in here"}), 403

        session["user"] = user.email
        session["logged_in"] = True
        session["role"] = user.role.value
        return jsonify({"message": "Logged in as admin"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 403

@users_bp.route("/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200


# API ADMINISTRATIVE FUNCTIONS (after admin login)
@users_bp.route("/register", methods=["POST"])
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
            role=data.get("role", "user")  # może być string
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_user.create()
    return jsonify({
        "message": f"User {new_user.email} registered",
        "role": new_user.role.value
    }), 201