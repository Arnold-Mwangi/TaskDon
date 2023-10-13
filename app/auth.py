
import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user_type = request.form['user_type']
        password = request.form['password']
        db = get_db
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required'
        elif not email:
            error = "Email is required"
        elif not user_type:
            error = "User type is required"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, email, user_type, password) VALUES(?, ?, ?, ?)",
                    (username, email, user_type, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
        return {'message': 'User registered successfully'}


