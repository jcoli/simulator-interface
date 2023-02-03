"""
Version: 0a
Tecnocoli - @11/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
Digital Simulator
func_time
"""

import time
from PyQt5.QtCore import QTime
from functions.basic_controls import btn_send

import time
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
text_date = datetime.now().strftime('%d-%m-%Y')
scanner_file = 'simulator-' + text_date+'.log'
handler = logging.FileHandler(scanner_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def timer_1(window):

    if not window.var1.in_a[0]:
        window.var1.mil_lamp = not window.var1.mil_lamp
        if window.var1.mil_lamp:
            window.led_mil.hide()
        else:
            window.led_mil.show()
    else:
        window.led_mil.hide()
    if window.var1.inj1:
        window.var1.inj1_show = not window.var1.inj1_show;
        if window.var1.inj1_show:
            window.injector_1_a.show()
            window.spark_1_a.show()
        else:
            window.injector_1_a.hide()
            window.spark_1_a.hide()
    else:
        window.injector_1_a.hide()
        window.spark_1_a.hide()

    time = QTime.currentTime()
    text = time.toString('hh:mm:ss')
    if (time.second() % 2) == 0:
        text = text[:2] + ' ' + text[3:]
    window.lcdTime.display(text)
    if window.var1.conected:
        btn_send(window, window.ser, "live")
        if not window.var1.bit_alive:
            window.var1.livebit_tmp = window.var1.livebit_tmp + 1
        if window.var1.bit_alive:
            window.var1.bit_alive = False
            window.var1.livebit_tmp = 0
            window.var1.conn_timeout = 20
            # window.btnStopGo.setEnabled(False)
        if window.var1.livebit_tmp >= window.var1.conn_timeout:
            logger.info("live timeout")
            window.var1.thread_flag = 'paused'
            window.append_text_ptd_datetime("not alive")
            window.var1.conected = False
            window.append_text_ptd_datetime("not ok livebit")
            window.btnStopGo.setEnabled(False)
            window.led_conn_simu_2.hide()
            window.status_bar.setStyleSheet("background-color: rgb(246, 11, 11);")
            window.status_bar.showMessage('Connection Error')
            window.btnConnect.setEnabled(True)
            window.append_text_ptd_datetime("serial timeout")
            window.btnConnect.setText("Conectar")
            window.var1.inject_live = False
            window.led_conn_simu_inj.hide()

    else:
        window.append_text_ptd_datetime("not alive")
        # window.var1.conected = False
        # window.append_text_ptd_datetime("not ok livebit")
        # window.btnStopGo.setEnabled(False)
        # window.led_conn_simu_2.hide()
        # window.status_bar.setStyleSheet("background-color: rgb(246, 11, 11);")
        # window.status_bar.showMessage('Connection Error')
        # window.btnConnect.setEnabled(True)
        # window.append_text_ptd_datetime("serial timeout")
        # window.btnConnect.setText("Conectar")
        # window.var1.inject_live = False
        # window.led_conn_simu_inj.hide()