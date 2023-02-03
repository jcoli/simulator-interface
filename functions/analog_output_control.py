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


def serial_output_ana(window, value_serial):
    try:
        # logger.info("serial_ouput_events ")
        # logger.info(value_serial)
        if "po" in str(value_serial):
            ret_txt = str(value_serial).split(",")
            output_ana(window, ret_txt[1], ret_txt[2])

    except Exception as e:
        if window.var1.debug:
            logger.info("Error serial_ouput_events " + str(e))


def output_ana(window, pot, level):
    try:
        logger.info("output ana: " + pot + " - " + level)
        sli_val = int(float(level))
        window.var1.ana_out[int(pot)] = sli_val
        objectName = "slider_" + str(pot)
        window.findChild(QObject, objectName).setValue(window.var1.ana_out[int(pot)])

        objectName = "slival_" + str(pot)
        propertyName = "setText"
        window.findChild(QObject, objectName).setText(str(window.var1.ana_out[int(pot)]))

    except Exception as e:
        if window.var1.debug:
            logger.info("Error output ana error 2: " + str(e))


def output_ana_send_serial(window, slider_name):
    try:
        if window.var1.debug:
            logger.info("output ana send: " + str(slider_name))
        point = slider_name[-1]
        pot = int(point)
        objectName = "slider_" + str(pot)
        level = window.findChild(QObject, objectName).value()
        send_txt = "po," + str(pot)+","+ str(level) + ",#"
        btn_send(window, window.ser, send_txt)

    except Exception as e:
        if window.var1.debug:
            logger.info("Error output ana error 1: " + str(e))