"""
Version: 0a
Tecnocoli - @07/2020
Author: Jeferson Coli - jcoli@tecnocoli.com.br
SPEED SENSOR SIMULATOR - camshafts and crankshafts - Arduino Uno/Nano
Function gen_pattern
"""

from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox

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
page = 0


# def start_pat(window, teeth):
#     window.pattern_pt = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
#     window.pattern_p = ""
#     window.line_gen_edges.setText(str(teeth))
#     if len(window.line_gen_edges.text()) > 0 :
#         window.edges = int(window.line_gen_edges.text())
#         if int(window.edges/10) == (window.edges/10):
#             window.max_pages = int(window.edges/10)
#         else:
#             window.max_pages = int(window.edges / 10)+1
#         window.edges_last_page = window.edges-((window.max_pages-1)*10)
#         if window.var1.debug:
#             window.append_text_ptd_datetime("edges changed: " + str(window.edges) + " - " + str(window.max_pages)
#                                        + " - " + str(window.edges_last_page))
#         window.btn_clear_pat.setEnabled(True)
#         window.btn_gen_pat.setEnabled(True)
#         # window.btn_prior_pat.setEnabled(True)
#         window.btn_next_pat.setEnabled(True)
#         window.btn_start_pat.setEnabled(False)
#         window.line_gen_edges.setEnabled(False)
#         window.page_pattern = 1
#         window.lbl_pag.setText(str(window.page_pattern))
#         window.textEdit_gen_pattern.setPlainText("")
#
#         for x in range(0, 10):
#             for i in range(1, 5):
#                 objectName = "cb" + str(x) + "0" + str(i)
#                 propertyName = "enabled"
#                 # window.append_text_ptd_datetime("Hide: " + str(x) + " - " + str(i))
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 objectName = "cb" + str(x) + "1" + str(i)
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#         for i in range(1, 5):
#             objectName = "cb" + "00" + str(i) + "_t"
#             propertyName = "enabled"
#             # window.append_text_ptd_datetime("Hide: " + str(x) + " - " + str(i))
#             window.findChild(QObject, objectName).setProperty(propertyName, True)
#             objectName = "cb" + "01" + str(i) + "_t"
#             window.findChild(QObject, objectName).setProperty(propertyName, True)
#
#
# def edit_pat(window, teeth, pattern):
#     logger.info("edit pat: " + str(pattern) + " - " + str(len(pattern)) + " - " + str(teeth))
#     window.pattern_pt = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
#     window.pattern_p = ""
#     window.line_gen_edges.setText(str(teeth))
#     if len(window.line_gen_edges.text()) > 0 :
#         window.edges = int(window.line_gen_edges.text())
#         if int(window.edges/10) == (window.edges/10):
#             window.max_pages = int(window.edges/10)
#         else:
#             window.max_pages = int(window.edges / 10)+1
#         window.edges_last_page = window.edges-((window.max_pages-1)*10)
#         logger.info("edit pat 2: " + str(window.max_pages))
#         pattern_temp = (pattern.split(","))
#         pattern_temp2 = " "
#         for i in range(0, len(pattern_temp) - 1):
#             pattern_temp2 = pattern_temp2 + (pattern_temp[i]) + ","
#         logger.info("gen_pattern_pt 1 " + str(pattern_temp))
#         logger.info("gen_pattern_pt 2 " + str(pattern_temp2))
#         for i in range(1, window.max_pages + 1):
#             if window.var1.debug:
#                 b = int(i * 40)
#                 a = b - 40 + 1
#                 logger.info("gen_pattern_pt 3 " + str(i) + " -a:" + str(a) + " -b:" + str(b))
#                 window.pattern_p = pattern_temp2[a:b]
#                 logger.info("gen_pattern_pt 4 " + str(window.pattern_p))
#                 window.pattern_pt[i - 1] = window.pattern_p
#                 logger.info("gen_pattern_pt 5 " + str(window.pattern_pt))
#
#         if window.var1.debug:
#             logger.info("edges changed: " + str(window.edges) + " - " + str(window.max_pages)
#                                        + " - " + str(window.edges_last_page))
#
#         window.btn_clear_pat.setEnabled(True)
#         window.btn_gen_pat.setEnabled(True)
#         # window.btn_prior_pat.setEnabled(True)
#         window.btn_next_pat.setEnabled(True)
#         window.btn_start_pat.setEnabled(False)
#         window.line_gen_edges.setEnabled(False)
#         window.page_pattern = 1
#         window.lbl_pag.setText(str(window.page_pattern))
#         window.textEdit_gen_pattern.setPlainText(str(pattern))
#         page_control_prior(window)
#
#     else:
#         error_msg_box = QMessageBox.Critical(window, 'Window Close', 'Tem certeza que deseja fechar o aplicativo?',
#                                             QMessageBox.OK)
#         # quit_msg_box = QMessageBox()
#         # quit_msg_box.setText("Tem certeza que deseja fechar o aplicativo?")
#         # quit_msg_box.addButton(QtWidgets.QStandardButton("Sim"), QtWidgets.QMessageBox.Yes)
#         # quit_msg_box.addButton(QtWidgets.QPushButton("Não"), QtGui.QMessageBox.No)
#         #
#         # QMessageBox.Yes.setText("Sim")
#
#         reply = error_msg_box
#
#
#
#
#
#
#
# def clean_pat(window):
#     window.max_pages = 1
#     window.pattern_pt = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
#     window.pattern_p = ""
#     window.textEdit_gen_pattern.setPlainText("")
#     window.btn_clear_pat.setEnabled(False)
#     window.btn_gen_pat.setEnabled(False)
#     window.btn_prior_pat.setEnabled(False)
#     window.btn_next_pat.setEnabled(False)
#     window.btn_start_pat.setEnabled(True)
#     window.line_gen_edges.setEnabled(True)
#
#     for x in range(0, 10):
#         for i in range(1, 5):
#             objectName = "cb" + str(x) + "0" + str(i)
#             propertyName = "enabled"
#             # window.append_text_ptd_datetime("Hide: " + str(x) + " - " + str(i))
#             window.findChild(QObject, objectName).setProperty(propertyName, False)
#             objectName = "cb" + str(x) + "1" + str(i)
#             window.findChild(QObject, objectName).setProperty(propertyName, False)
#     for i in range(1, 5):
#         objectName = "cb" + "00" + str(i) + "_t"
#         propertyName = "enabled"
#         # window.append_text_ptd_datetime("Hide: " + str(x) + " - " + str(i))
#         window.findChild(QObject, objectName).setProperty(propertyName, False)
#         objectName = "cb" + "01" + str(i) + "_t"
#         window.findChild(QObject, objectName).setProperty(propertyName, False)
#     clean_cb_pat(window)
#
# def btn_gen_pattern(window):
#     pattern = gen_pattern(window)
#     window.pattern_pt[window.page_pattern - 1] = pattern;
#     gen_pattern_pt(window)
#
# def btn_next(window):
#     pattern = gen_pattern(window)
#     window.pattern_pt[window.page_pattern - 1] = pattern;
#     if window.page_pattern < window.max_pages:
#         window.page_pattern = window.page_pattern + 1
#         window.lbl_pag.setText(str(window.page_pattern))
#         page_control_next(window)
#     if window.page_pattern == window.max_pages:
#         window.btn_next_pat.setEnabled(False)
#     window.btn_prior_pat.setEnabled(True)
#     gen_pattern_pt(window)
#     window.pattern_p = ""
#
# def btn_prior(window):
#     pattern = gen_pattern(window)
#     window.append_text_ptd_datetime("prior button " + pattern)
#     window.pattern_pt[window.page_pattern - 1] = pattern
#     if window.page_pattern > 1:
#         window.page_pattern = window.page_pattern - 1
#         window.lbl_pag.setText(str(window.page_pattern))
#         page_control_prior(window)
#     if window.page_pattern == 1:
#         window.btn_prior_pat.setEnabled(False)
#     window.btn_next_pat.setEnabled(True)
#     gen_pattern_pt(window)
#     window.pattern_p = ""
#
#
# def gen_pattern(window):
#     window.append_text_ptd_datetime("gen pattern button ")
#     window.pattern_p = ""
#     if window.page_pattern == window.max_pages:
#         for x in range(0 , window.edges_last_page):
#             edge0 = 0;
#             edge1 = 0;
#             for i in range(1 , 5):
#                 objectName = "cb" + str(x) + "0" + str(i)
#                 propertyName = "checked"
#                 cbCheck = bool(window.findChild(QObject, objectName).property(propertyName))
#                 if cbCheck:
#                     edge0 = edge0 + (2 ** (i - 1))
#                 objectName = "cb" + str(x) + "1" + str(i)
#                 cbCheck = bool(window.findChild(QObject, objectName).property(propertyName))
#                 if cbCheck:
#                     edge1 = edge1 + (2 ** (i - 1))
#             window.pattern_p = window.pattern_p + str(edge0) + ","
#             window.pattern_p = window.pattern_p + str(edge1) + ","
#             # window.textEdit_gen_pattern.setPlainText(window.textEdit_gen_pattern.toPlainText() + str(edge0) + ",")
#             # window.textEdit_gen_pattern.setPlainText(window.textEdit_gen_pattern.toPlainText() + str(edge1) + ",")
#     else:
#         for x in range(0, 10):
#             edge0 = 0;
#             edge1 = 0;
#             for i in range(1, 5):
#                 objectName = "cb" + str(x) + "0" + str(i)
#                 propertyName = "checked"
#                 cbCheck = bool(window.findChild(QObject, objectName).property(propertyName))
#                 if cbCheck:
#                     edge0 = edge0 + (2 ** (i - 1))
#                 objectName = "cb" + str(x) + "1" + str(i)
#                 cbCheck = bool(window.findChild(QObject, objectName).property(propertyName))
#                 if cbCheck:
#                     edge1 = edge1 + (2 ** (i - 1))
#             window.pattern_p = window.pattern_p + str(edge0) + ","
#             window.pattern_p = window.pattern_p + str(edge1) + ","
#
#     return window.pattern_p
#
#
# def page_control_next(window):
#     pattern = (window.pattern_pt[window.page_pattern - 1]).split(",")
#     if window.var1.debug:
#         logger.info("page control next: " + str(window.page_pattern) + " - " + str(len(pattern)) + " - "
#                                    + window.pattern_pt[window.page_pattern - 1])
#         logger.info("page control next: " + str(window.pattern_pt))
#     for i in range(1, 5):
#         propertyName = "checked"
#         objectName1 = "cb" + "00" + str(i) + "_t"
#         window.findChild(QObject, objectName1).setProperty(propertyName, False)
#         objectName1 = "cb" + "01" + str(i) + "_t"
#         window.findChild(QObject, objectName1).setProperty(propertyName, False)
#
#     if window.page_pattern == window.max_pages:
#         for x in range(window.edges_last_page, 10):
#             for i in range(1, 5):
#                 objectName = "cb" + str(x) + "0" + str(i)
#                 propertyName = "enabled"
#                 # window.append_text_ptd_datetime("Hide: " + str(x) + " - " + str(i))
#                 window.findChild(QObject, objectName).setProperty(propertyName, False)
#                 objectName = "cb" + str(x) + "1" + str(i)
#                 window.findChild(QObject, objectName).setProperty(propertyName, False)
#
#         for x in range(0, window.edges_last_page):
#             if len(pattern) > 1:
#                 edge0 = pattern[x * 2];
#                 edge1 = pattern[(x * 2) + 1];
#             else:
#                 edge0 = "0"
#                 edge1 = "0"
#             for i in range(1, 5):
#                 bin_mask = 2 ** (i - 1)
#
#                 cb_check_0 = bin_mask & int(edge0)
#                 cb_check_1 = bin_mask & int(edge1)
#                 objectName = "cb" + str(x) + "0" + str(i)
#                 propertyName = "enabled"
#                 # window.append_text_ptd_datetime("Hide: " + str(x) + " - " + str(i))
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 propertyName = "checked"
#                 if cb_check_0 > 0:
#                     window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 else:
#                     window.findChild(QObject, objectName).setProperty(propertyName, False)
#                 objectName = "cb" + str(x) + "1" + str(i)
#                 propertyName = "enabled"
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 propertyName = "checked"
#                 if cb_check_1 > 0:
#                     window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 else:
#                     window.findChild(QObject, objectName).setProperty(propertyName, False)
#                 if window.var1.debug:
#                     logger.info("page control next: " + str(x) + " - " + str(i) + " - " + edge0 + " - "
#                                                + edge1 + " - " + str(bin_mask) + " - " + str(cb_check_0)
#                                                + " - " + str(cb_check_1))
#     else:
#         for x in range(0, 10):
#             if len(pattern) > 1:
#                 edge0 = pattern[x * 2];
#                 edge1 = pattern[(x * 2) + 1];
#             else:
#                 edge0 = "0"
#                 edge1 = "0"
#             for i in range(1, 5):
#                 bin_mask = 2 ** (i - 1)
#                 cb_check_0 = bin_mask & int(edge0)
#                 cb_check_1 = bin_mask & int(edge1)
#                 objectName = "cb" + str(x) + "0" + str(i)
#                 propertyName = "enabled"
#                 # window.append_text_ptd_datetime("Hide: " + str(x) + " - " + str(i))
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 propertyName = "checked"
#                 if cb_check_0 > 0:
#                     window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 else:
#                     window.findChild(QObject, objectName).setProperty(propertyName, False)
#                 objectName = "cb" + str(x) + "1" + str(i)
#                 propertyName = "enabled"
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 propertyName = "checked"
#                 if cb_check_1 > 0:
#                     window.findChild(QObject, objectName).setProperty(propertyName, True)
#                 else:
#                     window.findChild(QObject, objectName).setProperty(propertyName, False)
#                 if window.var1.debug:
#                     if window.var1.debug:
#                         logger.info("page control next: " + str(x) + " - " + str(i) + " - " + edge0 + " - "
#                                                + edge1 + " - " + str(bin_mask) + " - " + str(cb_check_0)
#                                                + " - " + str(cb_check_1))
#
#
# def page_control_prior(window):
#     pattern = (window.pattern_pt[window.page_pattern-1]).split(",")
#     if window.var1.debug:
#         logger.info("page control prior: " + str(window.page_pattern) + " - " + str(len(pattern)) + " - "
#                                    + window.pattern_pt[window.page_pattern-1])
#     for i in range(1, 5):
#         propertyName = "checked"
#         objectName1 = "cb" + "00" + str(i) + "_t"
#         window.findChild(QObject, objectName1).setProperty(propertyName, False)
#         objectName1 = "cb" + "01" + str(i) + "_t"
#         window.findChild(QObject, objectName1).setProperty(propertyName, False)
#     for x in range(0, 10):
#         edge0 = pattern[x * 2];
#         edge1 = pattern[(x * 2) + 1];
#         for i in range(1, 5):
#             bin_mask = 2 ** (i-1)
#             cb_check_0 = bin_mask & int(edge0)
#             cb_check_1 = bin_mask & int(edge1)
#             objectName = "cb" + str(x) + "0" + str(i)
#             propertyName = "enabled"
#             # window.append_text_ptd_datetime("Hide: " + str(x) + " - " + str(i))
#             window.findChild(QObject, objectName).setProperty(propertyName, True)
#             propertyName = "checked"
#             if cb_check_0 > 0:
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#             else:
#                 window.findChild(QObject, objectName).setProperty(propertyName, False)
#             objectName = "cb" + str(x) + "1" + str(i)
#             propertyName = "enabled"
#             window.findChild(QObject, objectName).setProperty(propertyName, True)
#             propertyName = "checked"
#             if cb_check_1 > 0:
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#             else:
#                 window.findChild(QObject, objectName).setProperty(propertyName, False)
#             if window.var1.debug:
#                 window.append_text_ptd_datetime("page control prior: " + str(x) + " - " + str(i) + " - " + edge0 + " - "
#                                            + edge1 + " - " + str(bin_mask) + " - " + str(cb_check_0)
#                                            + " - " + str(cb_check_1))
#
#
# def gen_pattern_pt(window):
#     if window.var1.debug:
#         logger.info("gen_pattern_pt")
#         logger.info('gen_pattern_pt ' + str(window.max_pages))
#     window.textEdit_gen_pattern.setPlainText("")
#     for i in range(0, window.max_pages):
#         # logger.info('gen_pattern_pt ' + str(window.max_pages) + " - " + str(i) + " - " + window.pattern_pt[i])
#         window.textEdit_gen_pattern.setPlainText(window.textEdit_gen_pattern.toPlainText()+window.pattern_pt[i])
#         # window.append_text_ptd_datetime("gen_pattern_pt " + str(i))
#
#
# def clean_cb_pat(window):
#     if window.var1.debug:
#         logger.info("clear cb pattern")
#     # if (page == 0):
#     for x in range(0, 10):
#         edge0 = 0;
#         edge1 = 0;
#         for i in range(1, 5):
#             objectName = "cb" + str(x) + "0" + str(i)
#             propertyName = "checked"
#             window.findChild(QObject, objectName).setProperty(propertyName, False)
#             objectName = "cb" + str(x) + "1" + str(i)
#             window.findChild(QObject, objectName).setProperty(propertyName, False)
#             objectName1 = "cb" + "00" + str(i) + "_t"
#             window.findChild(QObject, objectName1).setProperty(propertyName, False)
#             objectName1 = "cb" + "01" + str(i) + "_t"
#             window.findChild(QObject, objectName1).setProperty(propertyName, False)
#
#
# def line_gen_edges_changed_pat(window):
#     if window.var1.debug:
#         window.append_text_ptd_datetime("edges changed: ")
#
#
# def cb000_t_clicked(window, edge, i):
#     if window.var1.debug:
#         window.append_text_ptd_datetime("cb000_clicked: " + str(i) + " - " + str(edge))
#
#     if edge == 0:
#         if window.var1.debug:
#             window.append_text_ptd_datetime("cb000_clicked:  edge 0")
#         objectName1 = "cb" + "00" + str(i) + "_t"
#         propertyName = "checked"
#         cbCheck = bool(window.findChild(QObject, objectName1).property(propertyName))
#
#         for x in range(0, 10):
#             objectName = "cb" + str(x) + "0" + str(i)
#             propertyName = "checked"
#             if cbCheck:
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#             else:
#                 window.findChild(QObject, objectName).setProperty(propertyName, False)
#
#     if edge == 1:
#         if window.var1.debug:
#             window.append_text_ptd_datetime("cb000_clicked:  edge 1")
#         objectName1 = "cb" + "01" + str(i) + "_t"
#         propertyName = "checked"
#         cbCheck = bool(window.findChild(QObject, objectName1).property(propertyName))
#
#         for x in range(0, 10):
#             objectName = "cb" + str(x) + "1" + str(i)
#             propertyName = "checked"
#             if cbCheck:
#                 window.findChild(QObject, objectName).setProperty(propertyName, True)
#             else:
#                 window.findChild(QObject, objectName).setProperty(propertyName, False)
#
