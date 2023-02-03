"""
Version: 0a
Tecnocoli - @07/2020
Author: Jeferson Coli - jcoli@tecnocoli.com.br
SPEED SENSOR SIMULATOR - camshafts and crankshafts - Arduino Uno/Nano
Function conn_serial
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
from functions.input_dig_control import serial_input_dig, input_port_a
from functions.output_dig_control import serial_output_dig, output_port_c
from functions.analog_output_control import serial_output_ana
from functions.analog_input_control import serial_input_ana
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
text_date = datetime.now().strftime('%d-%m-%Y')
scanner_file = 'simulator-' + text_date+'.log'
handler = logging.FileHandler(scanner_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



def scan_serial(window):
    """scan for available ports. return a list of serial names"""
    if window.var1.debug:
        logger.info('Scan Serial')
    try:
        """    
        ports = list(serial.tools.list_ports.comports())
        i = 0
        for port_no, description, address in ports:
            logger.info('port_no '+port_no)
            logger.info('description ' + description)
            logger.info('address ' + address)
            if 'Arduino Due Prog' in description:
                logger.info('this is Arduino Due ' + address)
        """
        com_ports_list = list(comports())
        ard_port = None
        prog_id = []
        # For Arduino Mega
        for port in com_ports_list:
            if window.var1.debug:
                logger.info('list ports ' + port[1] + ' - ' + port[0] + ' - ' + port[2])

            if port[1].startswith("GENERIC_F407VETX"):
            # if port[1].startswith("QinHeng Electronics HL-340"):
                ard_port = port  # Success; STM32F407 found

                if window.var1.debug:
                    logger.info('port_no 2 ' + port[1] + ' - ' + port[0])
                break  # stop searching-- we are done.
        if ard_port is None:
            for port in com_ports_list:
                if port[2].startswith("USB VID:PID=0483:5470"):
                # if port[2].startswith("USB VID:PID=1A86:7523"):
                    if window.var1.debug:
                        logger.info('port_no 3 ' + port[0])
                    ser = serial.Serial(port[0], 115200, timeout=2)
                    ser.write(b'sc,#')
                    time.sleep(0.3)
                    value_serial = ser.readline()
                    if window.var1.debug:
                        logger.info('port_no 4 ' + str(value_serial))
                    prog_id = str(value_serial).split(",")
                    logger.info("Connecting 5 " + str(value_serial))
                    if "sim" in prog_id[0]:
                        logger.info("Connecting 5 ")
                        ard_port = port # Success; Arduino Due found by VID/PID match.
                        break  # stop searching-- we are done.
        return ard_port

    except Exception as e:
        if window.var1.debug:
            logger.info("Error scan_serial " + str(e))
        # logger.info("Connected " + str(dig))
        return ard_port



def try_port(portStr):
    """returns boolean for port availability"""
    """test if has arduino due in port"""
    try:
        s = serial.Serial(portStr)
        s.close() # explicit close 'cause of delayed GC in java
        return True

    except serial.SerialException:
        pass
    except OSError as e:
        if e.errno != errno.ENOENT: # permit "no such file or directory" errors
            raise e

    return False


def serial_list_ports(window):
    if window.var1.debug:
        logger.info('list_ports')


def serial_read_events(window, value_serial):
    if window.var1.debug:
        if (("live" or "in") not in str(value_serial)) and window.var1.conected:
            logger.info(str("serial_read_events 1: " + str(value_serial)))
        # window.append_text_ptd_datetime(str("serial_read_events: " + str(value_serial)))
    try:
        if "live" in str(value_serial) and window.var1.conected:
            ret_txt = str(window.var1.value_serial).split(",")
            window.var1.bit_alive = True
            send_txt = 'live'
            btn_send(window, window.ser, send_txt)
            return

            # self.append_text_ptd_datetime("ALIVE")
        if "sim" in str(value_serial) and not window.var1.conected:
            # if window.var1.debug:
            #     logger.info('serial_read Simulator')
            window.prog_id = str(value_serial).split(",")
            window.append_text_ptd_datetime(window.prog_id[0])  # Nome
            window.var1.conected = True
            window.status_bar.setStyleSheet("background-color: rgb(112, 159, 252);")
            window.status_bar.clearMessage()
            window.status_bar.showMessage('Programador Conectado Versão: ' + window.prog_id[1] + ' - ' + window.prog_id[4])
            window.led_conn_simu_2.show()
            window.ser.write(b'id#')
            window.append_text_ptd_datetime("ok")
            window.btnStopGo.setEnabled(True)
            window.lcdRpm.display(str(window.next_rpm))
            time.sleep(0.5)
            window.append_text_ptd_datetime("ok 2")
            window.var1.thread_flag = 'go'
            return


        if "in" in str(value_serial):
            ret_txt = str(window.var1.value_serial).split(",")
            if "go" in ret_txt[1]:
                window.var1.stopGo = True
                window.btnStopGo.setText("Parar")
                window.led_conn_simu_inj.show()
                window.append_text_ptd_datetime("receive go: ")
                window.send_rpm = "rpm00050#"
                return
            elif "stop" in ret_txt[1]:
                window.var1.stopGo = False
                window.btnStopGo.setText("Acionar")
                window.led_conn_simu_inj.hide()
                window.append_text_ptd_datetime("receive stop: ")
                return
            elif "1" in ret_txt[1]:
                window.inject_live = True
                window.led_conn_inj_2.show()
                window.btnStopGo.setEnabled(True)
                window.btn_new_rpm.setEnabled(True)
                # if window.var1.debug:
                #     logger.info('Inject live true')
                return
            elif "0" in ret_txt[1]:
                window.inject_live = False
                window.led_conn_inj_2.hide()
                window.btnStopGo.setEnabled(False)
                window.btn_new_rpm.setEnabled(False)
                return



        if "L50" in str(value_serial):
            ret_txt = str(window.var1.value_serial).split(",")
            if "1" in ret_txt[1]:
                window.led_conn_l_50.show()
                window.var1.L50 = True
                window.btn_sim_L50.setText("Desligar")
                window.btn_sim_L30.setEnabled(True)
                return

            else:
                window.led_conn_l_50.hide()
                window.led_conn_l_30.hide()
                window.led_conn_l_15.hide()
                window.btn_sim_L50.setText("Ligar")
                window.var1.L50 = False
                window.btn_sim_L30.setEnabled(False)
                window.btn_sim_L15.setEnabled(False)
                return

        if "L30" in str(value_serial):
            ret_txt = str(window.var1.value_serial).split(",")
            if "1" in ret_txt[1]:
                window.led_conn_l_30.show()
                window.var1.L30 = True
                window.btn_sim_L30.setText("Desligar")
                window.btn_sim_L15.setEnabled(True)
                return
            else:
                window.led_conn_l_30.hide()
                window.led_conn_l_15.hide()
                window.var1.L30 = False
                window.btn_sim_L30.setText("Ligar")
                window.btn_sim_L15.setEnabled(False)
                return

        if "L15" in str(value_serial):
            ret_txt = str(window.var1.value_serial).split(",")
            if "1" in ret_txt[1]:
                window.led_conn_l_15.show()
                window.var1.L15 = True
                window.btn_sim_L15.setText("Desligar")
                return
            else:
                window.led_conn_l_15.hide()
                window.var1.L15 = False
                window.btn_sim_L15.setText("Ligar")
                return

        if "rpm" in str(value_serial):
            ret_txt = str(window.var1.value_serial).split(",")
            window.var1.next_rpm = int(ret_txt[1])
            window.lcdRpm.display(str(window.var1.next_rpm))
            window.line_new_rpm.setText(str(window.var1.next_rpm))
            window.slider_inj.setValue(window.var1.next_rpm)
            window.append_text_ptd_datetime("rpm" + str(window.var1.next_rpm))
            window.append_text_ptd_datetime("rpm slider" + str(window.slider_inj.value()))
            return

        # if "in" in str(value_serial):
        #     ret_txt = str(window.var1.value_serial).split(",")
        #     if "1" in ret_txt[1]:
        #         window.inject_live = True
        #         window.led_conn_inj_2.show()
        #         window.btnStopGo.setEnabled(True)
        #         window.btn_new_rpm.setEnabled(True)
        #         # if window.var1.debug:
        #         #     logger.info('Inject live true')
        #         return
        #     else:
        #         window.inject_live = False
        #         window.led_conn_inj_2.hide()
        #         window.btnStopGo.setEnabled(False)
        #         window.btn_new_rpm.setEnabled(False)
        #         if window.var1.debug:
        #                 window.append_text_ptd_datetime('Inject live false')
        #         # if window.var1.debug:
        #         #     logger.info('Inject live false')
        #         return

        if "p_put" in str(value_serial):
            if window.var1.debug:
                logger.info(str("serial - input_port_a: " ))
            input_port_a(window, value_serial)
        if "pc" in str(value_serial):
            serial_output_dig(window, value_serial)
        if "po" in str(value_serial):
            serial_output_ana(window, value_serial)
        if "ao" in str(value_serial):
            serial_input_ana(window, value_serial)
        if ("fu1" in str(value_serial)):
            # logger.info("Injetor 1")
            ret_txt = str(value_serial).split(",")
            if "1" in ret_txt[1]:
                window.var1.inj1 = True
                # logger.info("Injetor 1 True")
            else:
                window.var1.inj1 = False
                # logger.info("Injetor 1 False")
        if ("fu2" in str(value_serial)):
            # logger.info("Injetor 2")
            ret_txt = str(value_serial).split(",")
            if "1" in ret_txt[1]:
                window.var1.inj2 = True
                # logger.info("Injetor 2 True")
            else:
                window.var1.inj2 = False
                # logger.info("Injetor 2 False")
        if ("fu3" in str(value_serial)):
            # logger.info("Injetor 3")
            ret_txt = str(value_serial).split(",")
            if "1" in ret_txt[1]:
                window.var1.inj3 = True
                # logger.info("Injetor 3 True")
            else:
                window.var1.inj3 = False
                # logger.info("Injetor 3 False")
        if ("fu4" in str(value_serial)):
            # logger.info("Injetor 1")
            ret_txt = str(value_serial).split(",")
            if "1" in ret_txt[1]:
                window.var1.inj4 = True
                # logger.info("Injetor 4 True")
            else:
                window.var1.inj4 = False
                # logger.info("Injetor 4 False")
        if ("c1" in str(value_serial)):
            # logger.info("Coil 1")
            ret_txt = str(value_serial).split(",")
            if "1" in ret_txt[1]:
                window.var1.coil1 = True
                # logger.info("Coil 1 True")
            else:
                window.var1.coil1 = False
                # logger.info("Coil 1 False")
        if ("c2" in str(value_serial)):
            # logger.info("Coil 2")
            ret_txt = str(value_serial).split(",")
            if "1" in ret_txt[1]:
                window.var1.coil2 = True
                # logger.info("Coil 2 True")
            else:
                window.var1.coil2 = False
                # logger.info("Coil 2 False")
        if ("c3" in str(value_serial)):
            # logger.info("Coil 3")
            ret_txt = str(value_serial).split(",")
            if "1" in ret_txt[1]:
                window.var1.coil3 = True
                # logger.info("Coil 3 True")
            else:
                window.var1.coil3 = False
                # logger.info("Coil 3 False")
        if ("c4" in str(value_serial)):
            # logger.info("Coil 4")
            ret_txt = str(value_serial).split(",")
            if "1" in ret_txt[1]:
                window.var1.coil4 = True
                # logger.info("Coil 4 True")
            else:
                window.var1.coil4 = False
                # logger.info("Coil 4 False")
    except Exception as e:
        if window.var1.debug:
            logger.info("Error serial_read_events " + str(e))
        # self.append_text_ptp_datetime("Connection Error " + str(e))
        # self.status_bar.setStyleSheet("background-color: rgb(246, 11, 11);")
        # self.status_bar.showMessage('Connection Error Thread')


