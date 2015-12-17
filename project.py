from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Users, Disciplines, Journals, Base
#from oauth import *


engine = create_engine('sqlite:///journals.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

app = Flask(__name__)

@app.route('/')

def HomePage():
	allr = session.query(Journals).all()
	disciplines = session.query(Disciplines).all()
	return render_template('home.html', title = "HomePage", items = allr, disciplines = disciplines)

@app.route('/disciplines/<int:discipline_id>/')

def discipline(discipline_id):
	journals = session.query(Journals).filter_by(discipline_id = discipline_id)
	discipline_name = session.query(Disciplines).filter_by(id = discipline_id).one()
	return render_template("categories.html", title = discipline_name.name, items = journals, name = discipline_name.name)


@app.route('/journal/<int:journal_id>/')

def journalPage(journal_id):
	journal = session.query(Journals).filter_by(id = journal_id).one()
	if journal.picture is None:
		journal.picture = "default.jpg"
	discipline_name = session.query(Disciplines).filter_by(id = journal.discipline_id).one()
	return render_template('journal_page.html', title = journal.title, item = journal, discipline = discipline_name.name)



# @app.route('/login')

# # Create anti-forgery state token
# def showLogin():
#     state = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                     for x in xrange(32))
#     login_session['state'] = state
#     return render_template('login.html', STATE=state)

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)

