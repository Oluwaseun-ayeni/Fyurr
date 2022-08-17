from flask import Flask
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Password1!@localhost:5432/fyuur'
db = SQLAlchemy(app)






class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120),nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.ARRAY(db.String()))

    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    created_date = db.Column(db.DateTime, default = db.func.now())
    shows = db.relationship('Shows', backref='venue', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return f'Venue{self.name}' 

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):

    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))

    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    image_link = db.Column(db.String(500), nullable = False)
    facebook_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    seeking_description = db.Column(db.String(120))
    created_date = db.Column(db.DateTime, default = db.func.now())
    shows = db.relationship('Shows', backref='artist', lazy=True, cascade='all, delete-orphan')
   




class Shows(db.Model):


    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'),nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    show_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())    


db.create_all()