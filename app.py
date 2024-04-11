from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import desc
import math
import json
import os


app = Flask(__name__)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
    local_server = params.get("local_server", True)


app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/datahub'  # MySQL database URL
db = SQLAlchemy(app)


class Event(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(500))
    manager_name = db.Column(db.String(500))
    club_name = db.Column(db.String(100), nullable=True)
    event_date = db.Column(db.String(100))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    hall_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    ph_num = db.Column(db.BigInteger)
    department = db.Column(db.String(100), nullable=True)
    request = db.Column(db.DateTime)
    status = db.Column(db.String(255))


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    contactNo = db.Column(db.String(20), nullable=True)
    clubname = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)


class Venue(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    features = db.Column(db.String(255))
    imgfile = db.Column(db.String(255))

@app.route("/")
def home():
    venue = Venue.query.filter_by().all()
    last = math.ceil(len(venue)/int(params['no_of_posts']))
    

    page = request.args.get('page')

    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    venue = venue[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(params['no_of_posts'])]
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template('home.html', params=params, venue=venue, prev=prev, next=next)

@app.route("/venue")
def venue():
    venue = Venue.query.filter_by().all()
    last = math.ceil(len(venue)/int(params['no_of_posts']))
    

    page = request.args.get('page')

    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    venue = venue[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(params['no_of_posts'])]
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template('venue.html', params=params, venue=venue, prev=prev, next=next)

@app.route("/addvenue", methods=['GET','POST'])
def addvenue():
    if request.method == 'POST':
        name = request.form.get('name')
        capacity = request.form.get('capacity')
        features = request.form.get('features')
        imgfile = request.form.get('imgfile')

        f = request.files['file1']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        venue = Venue(name=name, capacity=capacity, features=features, imgfile=filename)
        db.session.add(venue)
        db.session.commit()
    return render_template('addvenue.html', params=params)


@app.route("/analytics")
def analytics():
    total_venues = Venue.query.count()
    total_bookings = Event.query.count()
    total_users = User.query.count()
    
    recent_bookings = Event.query.filter_by(status='accepted').order_by(desc(Event.request)).limit(5).all()
    return render_template("analytics.html", total_venues=total_venues, total_bookings=total_bookings, total_users=total_users,recent_bookings=recent_bookings)




if __name__ == "__main__":
    app.run(debug=True)