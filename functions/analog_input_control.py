"""
Version: 0a
Tecnocoli - @10/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
ECU SIMULATOR
Function inout_dig_control
"""

import serial
import serial.tools.list_ports
import errno
import string
import glob
import sys
import time
from datetime import datetime
import hashlib
from PyQt5.QtCore import *
import logging
from serial.tools.list_ports import comports
from functions.basic_controls import btn_send
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
text_date = datetime.now().strftime('%d-%m-%Y')
scanner_file = 'simulator-' + text_date+'.log'
handler = logging.FileHandler(scanner_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

from functions.bit_manip import testBit, setBit, clearBit, toggleBit


def serial_input_ana(window, value_serial):
    # if window.var1.debug:
    #         logger.info("serial_input_ana: " + str(value_serial))
    # window.append_text_ptd_datetime(str("serial_read_events: " + str(value_serial)))
    try:
        # if window.var1.debug:
        #     logger.info("serial_input_ana 1: ")
        if "ao" in str(value_serial):
            ret_txt = str(value_serial).split(",")
            # logger.info("serial_input_ana 1: " + str((ret_txt[1])))
            # logger.info("serial_input_ana 2: " + str((ret_txt[2])))
            # port_c_b = format(window.var1.port_c, 'b')
            # logger.info("serial_output_dig 1: "+str(ret_txt[1]))
            input_ana(window, ret_txt[1], ret_txt[3])

    except Exception as e:
        if window.var1.debug:
            logger.info("Error serial_input_analog_events " + str(e))
        # self.append_text_ptp_datetime("Connection Error " + str(e))
        # self.status_bar.setStyleSheet("background-color: rgb(246, 11, 11);")
        # self.status_bar.showMessage('Connection Error Thread')

def input_ana(window, ana_ref, level):
    try:
        # if window.var1.debug:
        #     logger.info("input_ana: " + str(ana_ref) + " - " + str(level))
        window.var1.ana_inp[int(ana_ref)] = level
        objectName = "ana_" + str(ana_ref)
        propertyName = "display"

        window.findChild(QObject, objectName).display(window.var1.ana_inp[int(ana_ref)])

    except Exception as e:
        if window.var1.debug:
            logger.info("Error input_ana_events " + str(e))