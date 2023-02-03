"""
Version: 0a
Tecnocoli - @11/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
Digital Simulator
Main
"""

from sqlalchemy import Column, Integer, String, BOOLEAN, REAL
from entities.base import Base


class InputAna(Base):
    __tablename__ = 'InputAna'
    id = Column(Integer, primary_key=True)
    addinp = Column(Integer)
    value = Column(REAL)
    chval = Column(BOOLEAN)
    conector = Column(String(20))
    pin_con = Column(String(20))
    cable = Column(String(20))
    wire = Column(String(20))
    descr = Column(String(20))
    type = Column(String(20))
    sensor = Column(String(20))

    def __init__(self, sensor):
        self.sensor = sensor
