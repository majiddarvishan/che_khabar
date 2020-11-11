"""Application routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models import User, db

@app.route("/", methods=["GET"])
def user_records():
    """Create a user via query string parameters."""
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    if email:
        existing_user = User.query.filter(
            User.email == email
        ).first()
        if existing_user:
            return make_response(f"{firstname} {lastname} ({email}) already created!")
        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days"
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for("user_records"))
    return render_template("users.jinja2", users=User.query.all(), title="Show Users")
