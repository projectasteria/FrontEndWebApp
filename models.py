from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
	"""
	Represents a user of the app
	"""
	__tablename__ = "user"
	id = Column(Integer, primary_key=True)
	username = Column(String(50), nullable=False, index=True, unique=True)
	password = Column(String(50),nullable=False)
	first_name = Column(String(50), nullable=False)
	last_name = Column(String(50),nullable=False)
	email = Column(String(128),nullable=False,unique=True)
	def __repr__(self):
		return "User {}".format(self.username)
    # def __repr__(self):
	# 	return "<User {}>".format(self.username)

