from flask import render_template, request, redirect, url_for, flash, session
from app.api.v2.users.model import User
from .auth import web_login_required
from .uploads import handle_upload
from .forms import EmailPasswordForm


def register_routes(app):
    @app.route("/")
    def home():
        form = EmailPasswordForm()
        return render_template("home.html", form=form)

    @app.route("/login", methods=["POST"])
    def login():
        form = EmailPasswordForm()
        if form.validate_on_submit():
            user = User.get_by_email(form.email.data)
            if user and user.check_password(form.password.data):
                session.clear()
                session["web_user_id"] = user.id
                session["web_email"] = user.email
                return redirect(url_for("home"))
        flash("Wrong credentials", "error")
        return redirect(url_for("home"))

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return redirect(url_for("home"))

    @app.route("/register", methods=["GET", "POST"])
    def create_user_view():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            if not email or not password:
                flash("E-mail and password are required", "error")
                return render_template("register.html")

            if User.get_by_email(email):
                flash("Cannot register", "error")
                return render_template("register.html")

            User.create_user(email, password)
            flash("User has been created", "success")
            return redirect(url_for("home"))

        return render_template("register.html")

    @app.route("/images/", methods=["GET", "POST"])
    @web_login_required
    def form_view():
        if request.method == "POST":
            if "file" not in request.files:
                return "no file part in the form", 400
            file = request.files["file"]
            if file.filename == "":
                return "no file selected", 400

            fname, size_bytes, sha = handle_upload(file)
            app.logger.info(
                f"UPLOADED: {fname}, size: {size_bytes} B, sha: {sha}"
            )
            return redirect(url_for("form_view"))

        return render_template("form_with_image.html")
