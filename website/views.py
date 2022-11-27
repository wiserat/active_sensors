from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Email
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        email = request.form.get('email')

        if len(email) < 1:
            flash('Email is too short!', category='error')
        else:
            new_email = Email(data=email, user_id=current_user.id)
            db.session.add(new_email)
            db.session.commit()
            flash('Email added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-email', methods=['POST'])
def delete_email():
    email = json.loads(request.data)
    emailId = email['emailId']
    email = Email.query.get(emailId)
    if email:
        if email.user_id == current_user.id:
            db.session.delete(email)
            db.session.commit()

    return jsonify({})
