#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import re
from urllib import response
import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from model import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


moment = Moment(app)
app.config.from_object('config')




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venue = Venue.query.get(Venue.city,Venue.state).all()
  data = []
  for search in venue:
    result ={
      'city':search.city,
      'state':search.state
    }
    data.append(result)
    print(data)

  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  text = request.get('search_term')
  search = Venue.query.filter(Venue.name.ilike(f'%{text}%')).all()
  count_len =len(search)

  response={
    'count':count_len,
    'data':[]
 
  }
  for s_response in search:
    search['data'].append ={
      'id':s_response.id,
      'name': s_response.name
    }
    

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  data = []
  for sh_venue in venue:
    response ={
      'id':sh_venue.id,
      'name':sh_venue.name
    }
    data.append(response)
 

  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
   new_venue = Venue(request.form['name'], request.form['city'],
    request.form['state'], request.form['address'], request.form['phone'], request.form['genres'],
    request.form['facebook_link'], request.form['website_link'], request.form['image_link'],
    request.form['seeking_description'], request.form['searching_talent'])
   db.session.add(new_venue)

   for verify in new_venue:
    if verify ==True:

     flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('Sorry venue cannot be listed, please try again') 
     
   return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  venue = Venue.query.get(venue_id)

  db.session.delete(venue)
  db.session.commit()
  flash('venue deletred successfully')
  
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  data=Artist.query(Artist.id,Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  artist_name = request.get('search_term')
  search = Artist.query.filter(Artist.name.ilike(f'%{artist_name}%')).all()
  count_len =len(search)

  response={
    'count':count_len,
    'data':[]
 
  }
  for s_response in search:
    search['data'].append ={
      'id':s_response.id,
      'name': s_response.name
    }
    

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  data = []
  for sh_artist in artist:
    response ={
      'id':sh_artist.id,
      'name':sh_artist.name
    }
    data.append(response)
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)


  id = request.form['id']  
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  website_link = request.form['website-link']
  seeking_talent = request.form['seeking_talent']
  facebook_link = request.form['facebook-link']
  image_link =request.form['image_link']

  artist.id = id
  artist.name = name
  artist.city = city
  artist.state = state
  artist.phone = phone
  artist.website_link = website_link
  artist.seeking_talent = seeking_talent
  artist.facebook_link = facebook_link
  artist.image_link = image_link

       


 
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  edited_artist = Artist.query.get(artist_id)

  try:  
    edited_artist.name = request.form('name')
    edited_artist.genres = request.form('genres')
    edited_artist.city = request.formt('city')
    edited_artist.phone = request.form('phone')
    edited_artist.state = request.form('state')
    edited_artist.website_link = request.form('website_link')
    edited_artist.seeking_talent = request.form('seeking_talent')
    edited_artist.seeking_description = request.form('seeking_description')
    edited_artist.facebook_link = request.form('facebook_link')
    edited_artist.image_link = request.form('image_link')
    db.session.add(edited_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + 'details has been succesfully updated!')
  except:
    flash('Error occur, try again')
  finally:  
    return redirect(url_for('show_artist', artist_id=artist_id))  
 

  

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)


  id = request.form['id']  
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  website_link = request.form['website-link']
  seeking_talent = request.form['seeking_talent']
  facebook_link = request.form['facebook-link']
  image_link =request.form['image_link']

  venue.id = id
  venue.name = name
  venue.city = city
  venue.state = state
  venue.phone = phone
  venue.website_link = website_link
  venue.seeking_talent = seeking_talent
  venue.facebook_link = facebook_link
  venue.image_link = image_link

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  edited_venue = Venue.query.get(venue_id)
  try:  
    edited_venue.name = request.form('name')
    edited_venue.genres = request.form('genres')
    edited_venue.city = request.formt('city')
    edited_venue.phone = request.form('phone')
    edited_venue.state = request.form('state')
    edited_venue.website_link = request.form('website_link')
    edited_venue.seeking_talent = request.form('seeking_talent')
    edited_venue.seeking_description = request.form('seeking_description')
    edited_venue.facebook_link = request.form('facebook_link')
    edited_venue.image_link = request.form('image_link')
    db.session.add(edited_venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + 'details has been succesfully updated!')
  except:
    flash('Error occur, try again')
  finally:  
    return redirect(url_for('show_venue', venue_id=venue_id))  
  
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  new_artist = Venue(request.form['name'], request.form['city'],
    request.form['state'], request.form['address'], request.form['phone'], request.form['genres'],
    request.form['facebook_link'], request.form['website_link'], request.form['image_link'],
    request.form['seeking_description'], request.form['searching_talent'])
  db.session.add(new_artist)

  for verify in new_artist:

    if verify ==True:

     flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('Sorry artist cannot be listed, please try again') 
 

 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  show_list = db.session.query(Shows).join(Artist).all()
  data = []

  for show in show_list:
    data.append({
      'venue_id': show.venue.id,
      'venue_name': show.venue.name,
      'artist_name': show.artist.name,
      'artist_id': show.artist_id,
      'artist_image_link': show.artist.image_link,
      'start_time': str(show.show_time.strftime('%Y -%m-%d %H:%M:S'))
    }) 
 

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  new_show = Shows(request.form['id'],request.form['venue_id'],request.form['artist_id'],
    request.form['show_time'])
  db.session.add(new_show)  
 
  for verify in new_show:

    if verify ==True:

     flash('Show was successfully listed!')
    else:
      flash('Sorry artist cannot be listed, please try again') 
 

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
