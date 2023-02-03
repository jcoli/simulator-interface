"""
Version: 0a
Tecnocoli - @07/2020
Author: Jeferson Coli - jcoli@tecnocoli.com.br
SPEED SENSOR SIMULATOR - camshafts and crankshafts - Arduino Uno/Nano
Function basic_controls
"""

from datetime import datetime
import serial
import time
from time import sleep
import hashlib


import logging
from serial.tools.list_ports import comports
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
text_date = datetime.now().strftime('%d-%m-%Y')
scanner_file = 'simulator-' + text_date+'.log'
handler = logging.FileHandler(scanner_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def btn_send(window, ser, send_txt):
    # logger.info('btn_send')
    try:
        txt_send = str.encode(send_txt + ',#')
        window.ser.write(txt_send)
        time.sleep(0.2)

    except Exception as e:
        if window.var1.debug:
            logger.info("Error connecting btn send:" + str(e))
        window.append_text_ptd_datetime("Sending Error")
        window.append_text_ptd_datetime(str(e))


def btn_connect(window, port, ser, prog_id):
    if window.var1.debug:
        logger.info('btn_connect')
    try:
        window.ser = serial.Serial(port[0], 115200, timeout=2)
        window.ser.write(b'sc,#')
        time.sleep(0.2)
        window.value_serial = window.ser.readline()
        window.var1.prog_id = str(window.value_serial).split(",")
        if "sim" in window.var1.prog_id[0]:
            # if window.var1.debug:
            #     logger.info("Simulator")
            # window.hash_id = hashlib.md5(window.var1.prog_id[3].encode())  # hashMD5 UniqueId
            # hex_dig = window.hash_id.hexdigest()
            # window.append_text_ptd_datetime(str(hex_dig))
            # dig = window.hash_id.digest()
            # window.append_text_ptd_datetime(str(dig))
            window.var1.conected = True
            window.status_bar.setStyleSheet("background-color: rgb(112, 159, 252); color: black ;")
            # window.status_bar.setStyleSheet("")
            window.status_bar.clearMessage()
            window.status_bar.showMessage('Simulador Conectado Versão: ' + window.var1.prog_id[1] + ' - ' + window.var1.prog_id[4])
            window.led_conn_simu_2.show()

            return "ok"
        else:
            # logger.info("---------"+window.var1.prog_id[0])
            window.status_bar.setStyleSheet("background-color: rgb(255,69,0); color: black ;")
            window.status_bar.clearMessage()
            window.status_bar.showMessage('Simulador não encontrado: ')
            window.led_conn_simu_2.show()
            window.ser.write(b'id#')
            return "not ok"

    except Exception as e:
        if window.var1.debug:
            logger.info("Error connecting btn connect: " + str(e))
        window.status_bar.setStyleSheet("background-color: rgb(246, 11, 11);")
        window.status_bar.showMessage('Connection Error')
        return "notok"

