from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from models import Base, Book

engine = create_engine('sqlite:///Books.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route("/")
@app.route("/books", methods = ['GET','POST'])
def book():
	if request.method == 'GET':
		return getAllBooks()

	elif request.method == 'POST':
		name = request.args.get("name")
		author = request.args.get("author")
		description = request.args.get("description")

		return addBook(name, author, description)


@app.route("/books/<int:book_id>", methods = ['GET','PUT','DELETE'])
def queryBook(book_id):

	if request.method == 'GET':
		return getBookWithId(book_id)

	elif request.method == 'PUT':

		name = request.args.get("name",None)
		author = request.args.get("author",None)
		description = request.args.get("description",None)

		return updateBook(book_id, name, author, description)

	elif request.method == 'DELETE':
		return deleteBook(book_id)

def getAllBooks():
	books = session.query(Book).all()
	return jsonify(Books = [i.serialize for i in books])

def addBook(name, author, description):
	mybook = Book(name = name, author = author, description = description)
	session.add(mybook)
	session.commit()

	return jsonify(Book = mybook.serialize)

def getBookWithId(id):
	mybook = session.query(Book).filter_by(id=id).one()
	return jsonify(Book = mybook.serialize)

def updateBook(id, name, author, description):
	mybook = session.query(Book).filter_by(id = id).one()
	if name!=None:
		mybook.name = name 
	
	if author!=None:
		mybook.author = author
	
	if description!=None:
		mybook.description = description
	

	session.add(mybook)
	session.commit()

	return jsonify(Book = mybook.serialize)

def deleteBook(id):
	mybook = session.query(Book).filter_by(id = id).one()
	session.delete(mybook)
	session.commit()

	return ("Removed Book with id %s" % id)

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000, debug = True)
