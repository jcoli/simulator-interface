"""
Version: 0a
Tecnocoli - @11/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
Digital Simulator
Main
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///database/injector.db", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

