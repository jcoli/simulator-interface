"""
Version: 0a
Tecnocoli - @11/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
Digital Simulator
Main
"""

from sqlalchemy import Column, Integer, String, REAL
from entities.base import Base



class Wheelpattern(Base):
    __tablename__ = 'wheelpattern'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    pattern = Column(String(500))
    short_desc = Column(String(20))
    long_desc = Column(String(60))
    edges = Column(Integer)
    teeth = Column(Integer)
    revolution = Column(Integer)
    rpmscaler = Column(REAL)

    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern
