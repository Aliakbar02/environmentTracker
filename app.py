from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Initialize Flask-Migrate
migrate = Migrate(app, db)
# Database model for complaints
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reporter_name = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=True)  # Latitude of the complaint location
    longitude = db.Column(db.Float, nullable=True) # Longitude of the complaint location
    is_solved = db.Column(db.Boolean, default=False)


# Routes
@app.route('/')
def index():
    complaints = Complaint.query.all()
    return render_template('index.html', complaints=complaints)

@app.route('/add', methods=['GET', 'POST'])
def add_complaint():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        reporter_name = request.form['reporter_name']

        new_complaint = Complaint(title=title, description=description, reporter_name=reporter_name)
        db.session.add(new_complaint)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add_complaint.html')

@app.route('/solve/<int:complaint_id>')
def solve_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.is_solved = True
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Establish application context before creating the database tables
    with app.app_context():
        db.create_all()  # Create all database tables
    app.run(debug=True)  # Start the Flask application
