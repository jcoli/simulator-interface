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


def serial_output_dig(window, value_serial):
    if window.var1.debug:
            logger.info("serial_output_dig 10: " + str(value_serial))
    # window.append_text_ptd_datetime(str("serial_read_events: " + str(value_serial)))
    try:
        if "pc" in str(value_serial):
            logger.info("serial_output_dig 2: ")
            ret_txt = str(value_serial).split(",")
            window.var1.port_c = int(ret_txt[1])

            serial_output_port_c(window)



    except Exception as e:
        if window.var1.debug:
            logger.info("Error serial_ouput_events " + str(e))
        # self.append_text_ptp_datetime("Connection Error " + str(e))
        # self.status_bar.setStyleSheet("background-color: rgb(246, 11, 11);")
        # self.status_bar.showMessage('Connection Error Thread')


def output_port_c(window, name):
    try:
        # if window.var1.debug:
        #     logger.info(str("output_port_c 1: " + str(window.var1.port_c)))
        point = name[-1]
        out = int(point)

        window.var1.oute_c[out] = not window.var1.oute_c[out]
        if window.var1.oute_c[out] > 0:
            window.var1.port_c = setBit(window.var1.port_c, out)
        else:
            window.var1.port_c = clearBit(window.var1.port_c, out)

        # for i in range(0, 7):
        #     objectName = "led_red_oute0" + str(i)
        #     # logger.info("output_: 2: " + objectName)
        #     if window.var1.oute_c[i] > 0:
        #         window.findChild(QObject, objectName).show()
        #         # logger.info("show")
        #     else:
        #         window.findChild(QObject, objectName).hide()
        #         # logger.info("hide")

        send_txt = "pc," + str(window.var1.port_c) + ",#"
        btn_send(window, window.ser, send_txt)
        if window.var1.debug:
            logger.info("output_port_c: " + str(window.var1.port_c) )

    except Exception as e:
        if window.var1.debug:
            logger.info("Error output port c error: " + str(e))


def serial_output_port_c(window):
    try:
        # if window.var1.debug:
        #     logger.info(str("output_port_c 1: " +str(window.var1.port_c)))

        for i in range(0, 8):
            objectName = "led_red_oute0" + str(i)
            objectName_chk = "chkBox_oute0" + str(i)
            window.var1.oute_c[i] = testBit(window.var1.port_c, i)
            if window.var1.oute_c[i] > 0:
                window.findChild(QObject, objectName).hide()
                window.findChild(QObject, objectName_chk).setChecked(True)
                # logger.info("show")
            else:
                window.findChild(QObject, objectName).show()
                window.findChild(QObject, objectName_chk).setChecked(False)
                # logger.info("hide")

        for i in range(8, 10):
            objectName = "led_red_oute0" + str(i)
            window.findChild(QObject, objectName).hide()
        for i in range(10, 18):
            objectName = "led_red_oute" + str(i)
            window.findChild(QObject, objectName).hide()

    except Exception as e:
        if window.var1.debug:
            logger.info("Error output port c error 1: " + str(e))
