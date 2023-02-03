"""
Version: 0a
Tecnocoli - @11/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
Digital Simulator
Main
"""

from sqlalchemy import Column, Integer, String, BOOLEAN, REAL
from entities.base import Base


class InputCoil(Base):
    __tablename__ = 'InputCoil'
    id = Column(Integer, primary_key=True)
    addinp = Column(Integer)
    value = Column(BOOLEAN)
    chval = Column(BOOLEAN)
    conector = Column(String(20))
    pin_con = Column(String(20))
    cable = Column(String(20))
    wire = Column(String(20))
    descr = Column(String(20))
    type = Column(String(20))
    sensor = Column(String(20))

    def __init__(self, addinp, value, chval, conector, pin_con, cable, wire, descr, type, sensor):
        self.addinp = addinp
        self.value = value
        self.chval = chval
        self.conector = conector
        self.pin_con = pin_con
        self.cable = cable
        self.wire = wire
        self.descr = descr
        self.type = type
        self.sensor = sensor
