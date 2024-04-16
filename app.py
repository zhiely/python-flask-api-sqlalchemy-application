from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "demand"
# Add database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
db = SQLAlchemy(app)
app.app_context().push()




# Create data model
class Events(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    event = db.Column(db.String(100),nullable=False)
    organizer = db.Column(db.String(100), nullable=False, default="default")
    date_added = db.Column(db.DateTime, default=datetime.now)

    #create string. returns a string representation of an event object, including its event attribute value
    def __repr__(self):
        return '<Event %r>' % self.name
    
# Import model from terminal (python, from app import db)
# db.create_all()


# Check if the database file exists
if not os.path.exists("events.db"):
    # Create all tables
    db.create_all()

    # Delete existing records from Events table
    db.session.query(Events).delete()
    db.session.commit()
# Create a form class
class EventForm(FlaskForm): #inherit FlaskForm from above
    event = StringField("Event",validators=[DataRequired()])
    submit = SubmitField("Submit")



# Route function- homepage
@app.route("/",methods=["POST","GET"])
def add_event():
    form = EventForm()
    
    if form.validate_on_submit():
            event = Events(event=form.event.data,organizer="default")
            db.session.add(event)
            db.session.commit()
            event = form.event.data
            form.event.data =''
            flash("Event Added Successfully!")
        #return redirect(url_for('add_event'))
    our_events = Events.query.order_by(Events.date_added)

    return render_template("add_event.html", form=form, our_events=our_events)

if __name__ == "__main__":

    app.run(debug=True)





