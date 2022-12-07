from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sensor_id = request.form.get('sensor_id_html')
        list_of_sensor_ids = []

        with open('website/sensor_ids.txt', 'r') as f:
            for line in f.readlines():
                list_of_sensor_ids.append(line.strip())
                
        if sensor_id not in list_of_sensor_ids:
            flash('Sensor ID does not exist', category='error')
        else:
            user = User.query.filter_by(sensor_id=sensor_id).first()
            if user:
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                try:
                    os.mkdir("all_emails_dir")
                except:
                    pass
                
                try:
                    with open(f'all_emails_dir/{current_user.id}_emails', 'x') as f:
                        f.close()
                except:
                    pass
               
                new_user = User(sensor_id=sensor_id)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Logged in!', category='success')
                return redirect(url_for('views.home'))
        
    return render_template("login.html", user=current_user)