import flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:/new.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<step {self.id}>'


@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', messages=Step.query.all())


@app.route('/steper', methods=['POST'])
def steper():
    steps = flask.request.form['steps']
    date = flask.request.form['date']
    db.session.add(Step(steps, date))
    db.session.commit()
    return flask.redirect(flask.url_for('steper'))


@app.route('/clear')
def clear():
    db.session.query(Step).delete()
    db.session.commit()
    return flask.redirect(flask.url_for('steper'))


with app.app_context():
    db.create_all()
app.run()
