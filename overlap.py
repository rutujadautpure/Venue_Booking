from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/eventscal'
db = SQLAlchemy(app)

class Event(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    manager_name = db.Column(db.String(100), nullable=False)
    club_name = db.Column(db.String(100), nullable=True)
    event_date = db.Column(db.DateTime(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)  # Change to db.Time
    end_time = db.Column(db.Time, nullable=False)    # Change to db.Time
    hall_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    ph_num = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    request = db.Column(db.String(500), nullable=True)


with app.app_context():
    db.create_all()  # Create tables based on the defined models

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle form submission
        event_name = request.form['eventName']
        manager_name = request.form['eventManagerName']
        club_name = request.form['orgClubName']
        event_date = request.form['eventDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        hall_name = request.form['hallName']  # Retrieve hall name from the form
        email = request.form['email']
        ph_num = request.form['phoneNumber']
        department = request.form['department']
        request_text = request.form['requestCreatedAt']

        # Check for event overlap at the same venue
        if not is_overlapping(event_date, start_time, end_time, hall_name):
            # Add new event to the database
            new_event = Event(event_name=event_name, manager_name=manager_name, club_name=club_name, event_date=event_date,
                              start_time=start_time, end_time=end_time, hall_name=hall_name, email=email,
                              ph_num=ph_num, department=department, request=request_text)
            db.session.add(new_event)
            db.session.commit()
            return "Event added successfully!"
        else:
            return "The event overlaps with an existing event at the same venue. Please choose another time."

    return render_template('overlap.html')


def is_overlapping(event_date, new_start_str, new_end_str, hall_name):
    new_start = datetime.strptime(new_start_str, '%H:%M').time()
    new_end = datetime.strptime(new_end_str, '%H:%M').time()

    events = Event.query.filter_by(event_date=event_date, hall_name=hall_name).all()
    for event in events:
        start_time = event.start_time.strftime('%H:%M')
        end_time = event.end_time.strftime('%H:%M')

        start_time = datetime.strptime(start_time, '%H:%M').time()
        end_time = datetime.strptime(end_time, '%H:%M').time()

        if (start_time <= new_start < end_time) or \
           (start_time < new_end <= end_time) or \
           (new_start <= start_time and new_end >= end_time):
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
