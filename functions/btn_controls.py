"""
Version: 0a
Tecnocoli - @11/2020
Author: Jeferson Coli - jcoli@tecnocoli.com.br
SPEED SENSOR SIMULATOR - camshafts and crankshafts - Arduino Uno/Nano
Function btn_controls
"""

from datetime import datetime
import serial
import time
from time import sleep
import hashlib
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
text_date = datetime.now().strftime('%d-%m-%Y')
scanner_file = 'simulator-' + text_date+'.log'
handler = logging.FileHandler(scanner_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



