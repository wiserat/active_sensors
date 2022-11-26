from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        sensor_id = request.form.get('sensor_id')
        list_of_sensor_ids = []
        with open('website/sensor_ids.txt', 'r') as f:
            for line in f.readlines():
                sensor_id_ = (line.rstrip())
                list_of_sensor_ids.append(sensor_id_)
        print(list_of_sensor_ids, sensor_id)
        if sensor_id not in list_of_sensor_ids:
            flash('Sensor ID not found', category='error')
        else:
            flash('Sensor ID found', category='success')
            
    return render_template("home.html")

@auth.route('/logout')
def logout():
    return render_template("logout.html")

@auth.route('/login')
def login():
    return render_template("login.html")