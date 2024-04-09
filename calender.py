from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/eventscal'  # MySQL database URL
db = SQLAlchemy(app)

# Define the Event model
from datetime import datetime

class Event(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.String(100), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.String(20), nullable=False)

# Function to fetch events from the database for a given date
def fetch_events_for_date(date):
    events = Event.query.filter_by(date=date).all()
    return [{'venue': event.venue, 'event_name': event.event_name} for event in events]

@app.route('/')
def index():
    return render_template('calender.html')

@app.route('/events', methods=['GET'])
def events():
    date = request.args.get('date')
    events_for_date = fetch_events_for_date(date)
    return jsonify(events_for_date)

if __name__ == '__main__':
    app.run(debug=True)
