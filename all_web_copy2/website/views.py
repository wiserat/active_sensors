from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Email
from . import db
import json
import os
from sqlalchemy.orm import load_only


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        email = request.form.get('email')

        if len(email) == 0:
            flash('Email is empty!', category='error')
        elif len(email) < 5:
            flash('Email is too short!', category='error')
        else:
            new_email = Email(data=email, user_id=current_user.id)
            db.session.add(new_email)
            db.session.commit()
            flash('Email added!', category='success')
            with open(f"all_emails_dir/{current_user.id}_emails", "a") as f:
                f.write(email + "\n")
            
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
            with open(f"all_emails_dir/{current_user.id}_emails", "r") as f:
                text = f.read()
                list = []
                for line in text.splitlines():

                    list.append(line)
                
                selected_email = email.data
                
            with open(f"all_emails_dir/{current_user.id}_emails", "w") as f:
                for line in list:
                    if line != selected_email:
                        f.write(line + "\n")

    return jsonify({})