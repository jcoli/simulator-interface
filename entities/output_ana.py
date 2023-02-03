"""
Version: 0a
Tecnocoli - @11/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
Digital Simulator
Main
"""

from sqlalchemy import Column, Integer, String, BOOLEAN
from entities.base import Base


class OutputAna(Base):
    __tablename__ = 'OutputAna'
    id = Column(Integer, primary_key=True)
    addout = Column(Integer)
    cs_pin = Column(Integer)
    val_pot = Column(Integer)
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