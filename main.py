"""
Version: 0a
Tecnocoli - @03/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
Digital Simulator
Main
"""
import sys
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableView, QMessageBox
from PyQt5.QtCore import QFile, QTimer, QTime, Qt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from pathlib import Path
from forms.MainWindow import Ui_MainWindow

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import obd
from obd import Unit, OBDResponse
from obd import ECU
from obd.protocols.protocol import Message
from obd.utils import OBDStatus
from obd.OBDCommand import OBDCommand
from obd.decoders import noop

# import sqlite3
import hashlib
import serial
from datetime import datetime
import time
from time import sleep
from functions.conn_serial import scan_serial, serial_list_ports, serial_read_events
from functions.basic_controls import btn_connect, btn_send
# from functions.gen_pattern import btn_next, btn_prior, btn_gen_pattern, \
#     line_gen_edges_changed_pat, start_pat, clean_pat, cb000_t_clicked
from functions.get_qtcss import get_style, available_styles
import functions.btn_controls
from functions.odbFunctions import *
from functions.func_time import timer_1
from functions.input_dig_control import serial_input_dig
from functions.output_dig_control import serial_output_dig, output_port_c
from functions.bit_manip import testBit, setBit, clearBit, toggleBit
from functions.analog_output_control import serial_output_ana, output_ana_send_serial


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

# entities
from entities.user import User
from entities.wheelpattern import Wheelpattern
from entities.input_digital import InputDigital
from entities.output_ana import OutputAna
from entities.input_ana import InputAna
from entities.ouput_digital import OutputDigital
from entities.input_Injector import InputInjector
from entities.input_coil import InputCoil
from entities.base import Session, engine, Base
Base.metadata.create_all(engine)
session = Session()

from functions.variables import Variables


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ser = serial.Serial();
        self.var1 = Variables
        self.setupUi(self)
        self.tab_bar.setCurrentIndex(0)
        if not self.var1.debug:
            self.tab_bar.removeTab(4)
        self.t1 = threading.Thread(target=self.task1)
        self.onlyInt = QIntValidator(0, 120, self)
        #self.tabDebug.setVisible(False)
        self.init_form()
        # self.showMaximized()
        # self.db = QSqlDatabase.addDatabase("QSQLITE")
        # self.modelWheel = QSqlQueryModel()
        # self.modelChoose = QSqlQueryModel()
        # self.db.setDatabaseName("database/injector.db")
        # self.model = QSqlTableModel(self, self.db)
        # if not self.db.open():
        #     print("db error")
        # else:
        #     print("db ok")

        timer: object = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)
        # timerReadODB: object = QTimer(self)
        # self.t1.start()



    def closeEvent(self, event):
        quit_msg_box = QMessageBox.question(self, 'Window Close', 'Tem certeza que deseja fechar o aplicativo?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        reply = quit_msg_box

        if reply == QMessageBox.Yes:
            btn_send(window, self.ser, "descon")
            time.sleep(0.2)
            event.accept()
            self.var1.thread_flag = "stop"
            time.sleep(0.7)
            if self.var1.debug:
                print('Window closed')
        else:
            event.ignore()

    def btn_sim_L50_clicked(self):
        if self.var1.L50:
            send_txt = 'L50,0,'
        else:
            send_txt = 'L50,1,'
        btn_send(window, self.ser, send_txt)

    def btn_sim_L30_clicked(self):
        if self.var1.L30:
            send_txt = 'L30,0,'
        else:
            send_txt = 'L30,1,'
        btn_send(window, self.ser, send_txt)

    def btn_sim_L15_clicked(self):
        if self.var1.L15:
            send_txt = 'L15,0,'
        else:
            send_txt = 'L15,1,'
        btn_send(window, self.ser, send_txt)

    def show_time(self):
        timer_1(window)

    def task1(self):
        try:
            if self.ser.isOpen():
                while True:
                    if self.var1.debug:
                        logger.info("Thread 1 waiting for permission to read")
                    while self.var1.thread_flag != 'go':
                        time.sleep(0.1)
                    if self.var1.debug:
                        logger.info("Thread 1 is waiting 1 " + self.var1.thread_flag)
                    while self.var1.thread_flag == 'go':
                        self.var1.value_serial = self.ser.readline().strip()
                        if len(self.var1.value_serial) > 0:
                            serial_read_events(window, self.var1.value_serial)
                        time.sleep(0.1) #was 0.3
                    if self.var1.thread_flag == 'stop':
                        break
                    else:
                        self.var1.thread_flag = 'paused'  # signals that the inner loop is done
                        # if self.var1.debug:
                        #     self.append_text_ptd_datetime(str("Paused"))
            else:
                if self.var1.debug:
                    logger.info("serial closed")
        except Exception as e:
            if self.var1.debug:
                logger.info("Error serial reading :" + str(e))

    def btn_stop_go_clicked(self):
        if self.var1.stopGo:
            send_txt = 'in,stop'
        else:
            send_txt = 'in,go'
        btn_send(window, self.ser, send_txt)

    def btn_connect_clicked(self):
        try:
            if not self.var1.conected:
                port = scan_serial(window)
                if self.var1.debug:
                    logger.info("Connecting 1 ")
                if port is not None:
                    time.sleep(0.5)
                    ret_txt = btn_connect(window, port, self.ser, self.var1.prog_id)
                    if "ok" in ret_txt:
                        if self.var1.debug:
                            logger.info("Connecting ok ")
                        time.sleep(0.5)
                        if not self.var1.thread_bit:
                            self.t1.start()
                            self.var1.thread_bit = True
                        time.sleep(0.5)
                        self.var1.thread_flag = 'go'
                        self.var1.bit_alive = True
                        self.var1.conected = True
                        self.btnConnect.setText("Desconectar")
                        self.btn_sim_L50.setEnabled(True)
                        btn_send(window, self.ser, 'id')

                    else:
                        if self.var1.debug:
                            logger.info("Connecting not ok connecting")
                        self.status_bar.setStyleSheet("background-color: rgb(255,69,0);")
                        self.status_bar.showMessage('Connection Error')
                else:
                    if self.var1.debug:
                        logger.info("Connecting 2 ")
                        logger.info('Não foi encontrado nenhum dispositivo compatível')
                    self.status_bar.setStyleSheet("background-color: rgb(255,140,0);")
                    self.status_bar.showMessage('Não foi encontrado nenhum dispositivo compatível')
            else:
                self.var1.conected = False
                self.var1.thread_flag = 'paused'
                self.var1.bit_alive = False
                self.btnConnect.setText("Conectar")
                btn_send(window, self.ser, "descon")
                self.status_bar.setStyleSheet("background-color: rgb(244, 255, 16);")
                self.status_bar.showMessage('Programador Desconectado')
                self.btnStopGo.setEnabled(False)
                self.btn_new_rpm.setEnabled(False)
                self.btn_sim_L50.setEnabled(False)
                self.btn_sim_L30.setEnabled(False)
                self.btn_sim_L15.setEnabled(False)
                self.led_conn_l_50.hide()
                self.led_conn_l_30.hide()
                self.led_conn_l_15.hide()
                self.var1.stopGo = False
                self.btnStopGo.setText("Acionar")
                self.led_conn_inj_2.hide()
                self.led_conn_simu_2.hide()
                self.injector_1_a.hide()
                self.injector_2_a.hide()
                self.injector_3_a.hide()
                self.injector_4_a.hide()
                self.spark_1_a.hide()
                self.spark_2_a.hide()
                self.spark_3_a.hide()
                self.spark_4_a.hide()
                self.var1.inject_live = False
        except Exception as e:
            if self.var1.debug:
                logger.info("Error connecting btn_connect_clicked" + str(e))
            self.status_bar.setStyleSheet("background-color: rgb(246, 11, 11);")
            self.status_bar.showMessage('Connection Error')

    def btn_new_rpm_clicked(self):
        # self.send_txt = 'nw'
        self.var1.next_rpm = int(self.line_new_rpm.text());
        if (self.var1.next_rpm < 1000):
            send_rpm = "rpm00" + str(self.var1.next_rpm) + "#"
        elif (self.var1.next_rpm >= 1000) and (self.var1.next_rpm < 10000):
            send_rpm = "rpm0" + str(self.var1.next_rpm) + "#"
        else:
            send_rpm = "rpm" + str(self.var1.next_rpm) + "#"
        self.lcdRpm.display(str(self.var1.next_rpm))
        self.slider_inj.setValue(self.var1.next_rpm)
        btn_send(window, self.ser, send_rpm)

    def slider_inj_change(self):
        widgetname = self.focusWidget().objectName()
        self.var1.next_rpm = self.slider_inj.value()
        if self.var1.next_rpm < 1000:
            send_rpm = "rpm00" + str(self.var1.next_rpm) + "#"
        elif (self.var1.next_rpm >= 1000) and (self.var1.next_rpm < 10000):
            send_rpm = "rpm0" + str(self.var1.next_rpm) + "#"
        else:
            send_rpm = "rpm" + str(self.var1.next_rpm) + "#"
        btn_send(window, self.ser, send_rpm)

    def btn_send_clicked(self):
        try:
            send_txt = self.lineEdit.text()
            btn_send(window, self.ser, send_txt)
        except Exception as e:
            logger.info("Error connecting ")
            logger.info(str(e))

    def oute00_clicked(self):
        widgetname = self.focusWidget().objectName()
        output_port_c(window, widgetname)

    def slider_change(self):
        widgetname = self.focusWidget().objectName()
        output_ana_send_serial(window, widgetname)

    def slider_clicked(self):
        if self.timer_id != -1:
            self.killTimer(self.timer_id)
        self.timer_id = self.startTimer(500)

    def slider_in_clicked(self):
        if self.timer_id_2 != -1:
            self.killTimer(self.timer_id_2)
        self.timer_id_2 = self.startTimer(500)

    def timerEvent(self, event):
        self.killTimer(self.timer_id)
        self.timer_id = -1
        self.slider_change()

    def timerEvent_2(self, event):
        self.killTimer(self.timer_id)
        self.timer_id = -1
        self.slider_inj_change()

    def init_form(self):
        self.timer_id = -1
        self.timer_id_2 = -1
        self.btnConnect.clicked.connect(self.btn_connect_clicked)
        self.btnStopGo.clicked.connect(self.btn_stop_go_clicked)
        self.btn_new_rpm.clicked.connect(self.btn_new_rpm_clicked)
        self.btn_sim_L50.clicked.connect(self.btn_sim_L50_clicked)
        self.btn_sim_L30.clicked.connect(self.btn_sim_L30_clicked)
        self.btn_sim_L15.clicked.connect(self.btn_sim_L15_clicked)
        self.chkBox_oute00.clicked.connect(self.oute00_clicked)
        self.chkBox_oute01.clicked.connect(self.oute00_clicked)
        self.chkBox_oute02.clicked.connect(self.oute00_clicked)
        self.chkBox_oute03.clicked.connect(self.oute00_clicked)
        self.chkBox_oute04.clicked.connect(self.oute00_clicked)
        self.chkBox_oute05.clicked.connect(self.oute00_clicked)
        self.chkBox_oute06.clicked.connect(self.oute00_clicked)
        self.chkBox_oute07.clicked.connect(self.oute00_clicked)
        self.slider_0.valueChanged.connect(self.slider_clicked)
        self.slider_1.valueChanged.connect(self.slider_clicked)
        self.slider_2.valueChanged.connect(self.slider_clicked)
        self.slider_3.valueChanged.connect(self.slider_clicked)
        self.slider_4.valueChanged.connect(self.slider_clicked)
        self.slider_5.valueChanged.connect(self.slider_clicked)
        self.slider_6.valueChanged.connect(self.slider_clicked)
        self.slider_7.valueChanged.connect(self.slider_clicked)
        self.slider_8.valueChanged.connect(self.slider_clicked)
        # self.slider_9.sliderReleased.connect(self.slider_00_change)
        self.slider_9.valueChanged.connect(self.slider_clicked)
        self.slider_inj.sliderReleased.connect(self.slider_inj_change)
        # self.slider_inj.valueChanged.connect(self.slider_in_clicked)

        self.btn_sim_L50.setEnabled(False)
        self.btn_sim_L30.setEnabled(False)
        self.btn_sim_L15.setEnabled(False)
        self.btnStopGo.setEnabled(False)
        self.btn_new_rpm.setEnabled(False)

        self.injector_1_a.hide()
        self.injector_2_a.hide()
        self.injector_3_a.hide()
        self.injector_4_a.hide()
        self.spark_1_a.hide()
        self.spark_2_a.hide()
        self.spark_3_a.hide()
        self.spark_4_a.hide()

        self.led_conn_simu_2.hide()
        self.led_conn_inj_2.hide()
        self.led_conn_l_50.hide()
        self.led_conn_l_30.hide()
        self.led_conn_l_15.hide()
        self.led_in00.hide()
        self.led_in01.hide()
        self.led_in02.hide()
        self.led_in03.hide()
        self.led_in04.hide()
        self.led_in05.hide()
        self.led_in06.hide()
        self.led_in07.hide()
        self.led_in08.hide()
        self.led_in09.hide()
        self.led_in10.hide()
        self.led_in11.hide()
        self.led_in12.hide()
        self.led_in13.hide()
        self.led_in14.hide()
        self.led_in15.hide()
        self.led_in16.hide()
        self.led_in17.hide()
        self.led_in18.hide()
        self.led_in19.hide()
        self.led_in20.hide()

        self.btnStopGo.setText("Acionar")
        self.led_conn_simu_inj.hide()
        self.status_bar.setStyleSheet("background-color: rgb(244, 255, 16); color: black ;")
        self.status_bar.showMessage('Simulador Desconectado')

        self.led_mil.hide()
        self.btn_new_rpm.setEnabled(False)
        self.line_new_rpm.setText("50")

    def append_text_ptd_datetime(self, pText):
        self.plainTextEdit_debug.appendPlainText(
            datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " --> " + pText)

# def time_thread(self):
#     timer: object = QTimer()
#     timer.timeout.connect(MainWindow.show_time)
#     timer.start(1000)
#     MainWindow.show_time(self)


app = QtWidgets.QApplication(sys.argv)
style_string = get_style("dark_blue")
app.setStyleSheet(style_string)
window = MainWindow()
window.show()
app.exec()
