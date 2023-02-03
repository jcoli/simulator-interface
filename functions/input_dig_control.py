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


def serial_input_dig(window, value_serial):
    # if window.var1.debug:
    #     if ("live" or "inject") not in str(value_serial) and window.conected:
    #         logger.info(str("serial_input_dig 1: " + str(value_serial)))
    # window.append_text_ptd_datetime(str("serial_read_events: " + str(value_serial)))
    try:

        # if window.var1.debug:
        #     logger.info('serial_input_dig')
        if "p_in" in str(value_serial):
            input_port_a(window, value_serial)
        # if "pk" in str(value_serial):
        #     input_port_k(window, value_serial)
        # if "pe" in str(value_serial):
        #     input_port_e(window, value_serial)
        # if "pg" in str(value_serial):
        #     input_port_g(window, value_serial)

    except Exception as e:
        if window.var1.debug:
            logger.info("Error serial_input_events " + str(e))
        # self.append_text_ptp_datetime("Connection Error " + str(e))
        # self.status_bar.setStyleSheet("background-color: rgb(246, 11, 11);")
        # self.status_bar.showMessage('Connection Error Thread')


def input_port_a(window, value_serial):
    try:
        if window.var1.debug:
            logger.info(str("input_port_a: " ))
        ret_txt = str(value_serial).split(",")
        window.var1.port_a = int(ret_txt[1])
        if window.var1.debug:
            logger.info(str("input_port_a: " + str(value_serial)) + " - " + str(window.var1.port_a))

        for i in range(0, 16):
            if i <= 9:
                objectName = "led_in0" + str(i)
            else:
                objectName = "led_in" + str(i)
            # logger.info("input a: 2: " + objectName)
            window.var1.in_a[i] = testBit(window.var1.port_a, i)
            if window.var1.in_a[i] > 0:
                window.findChild(QObject, objectName).hide()
                # logger.info("show")
            else:
                window.findChild(QObject, objectName).show()
                # logger.info("hide")

    except Exception as e:
        if window.var1.debug:
            logger.info("Error input porta " + str(e))
        ret_txt = str(window.value_serial).split(",")


# def input_port_k(window, value_serial):
#     try:
#         # if window.var1.debug:
#         #     logger.info(str("input_port_k: " + str(value_serial)))
#         ret_txt = str(value_serial).split(",")
#         # logger.info("input_port_k 1 " + ret_txt[0]+" - "+ret_txt[1])
#         window.var1.port_k = int(ret_txt[1])
#         # logger.info("input_port_k 1 ")
#         for i in range(8, 16):
#             if i < 10:
#                 objectName = "led_in0" + str(i)
#             else:
#                 objectName = "led_in" + str(i)
#
#             p = i - 8
#             # logger.info("input k: 2: " + objectName)
#
#             window.var1.in_k[i-8] = testBit(window.var1.port_k, i-8)
#             # logger.info("input k: 2: " + objectName)
#             if window.var1.in_k[i-8] > 0:
#                 window.findChild(QObject, objectName).hide()
#                 # logger.info("show")
#             else:
#                 window.findChild(QObject, objectName).show()
#                 # logger.info("hide")
#
#     except Exception as e:
#         if window.var1.debug:
#             logger.info("Error serial_input_k_events " + str(e))
#
#
# def input_port_e(window, value_serial):
#
#     try:
#         if window.var1.debug:
#             if "live" not in str(value_serial) and window.conected:
#                 logger.info(str("input_port_e: " + str(value_serial)))
#         ret_txt = str(value_serial).split(",")
#
#     except Exception as e:
#         if window.var1.debug:
#             logger.info("Error serial_read_events " + str(e))
#
#
# def input_port_g(window, value_serial):
#     try:
#         if window.var1.debug:
#             logger.info(str("input_port_g: " + str(value_serial)))
#         ret_txt = str(value_serial).split(",")
#
#     except Exception as e:
#         if window.var1.debug:
#             logger.info("Error serial_read_events " + str(e))
#
#
# def input_port_h(window, value_serial):
#     try:
#         if window.var1.debug:
#             logger.info(str("input_port_h: " + str(value_serial)))
#         ret_txt = str(value_serial).split(",")
#
#     except Exception as e:
#         if window.var1.debug:
#             logger.info("Error serial_read_events " + str(e))