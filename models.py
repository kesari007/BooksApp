from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Book(Base):
	__tablename__ = 'Books'

	name = Column(String(50), nullable = False)
	author = Column(String(50), nullable = False)
	description = Column(String(100))
	id = Column(Integer, primary_key = True)

	@property
	def serialize(self):
		return{
			'id' : self.id,
			'name' : self.name,
			'description': self.description,
			'author': self.author
		}

engine = create_engine('sqlite:///Books.db')
Base.metadata.create_all(engine)