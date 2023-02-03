"""
Version: 0a
Tecnocoli - @07/2020
Author: Jeferson Coli - jcoli@tecnocoli.com.br
SPEED SENSOR SIMULATOR - camshafts and crankshafts - Arduino Uno/Nano
Function db_controls
"""

from datetime import datetime
import time
from time import sleep
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from functions.gen_pattern import start_pat, edit_pat

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


def tableWheel_clicked_db(window):
    if window.var1.debug:
        logger.info('tableWheel_clicked_db')

    record = window.modelWheel.record(window.tableWheel.currentIndex().row())
    window.lineEdit_name.setText(record.value("name"))
    window.lineEdit_scaler.setText(str(record.value("rpmScaler")))
    window.lineEdit_dentes.setText(str(record.value("teeth")))
    window.textEdit_pattern.setText(record.value("pattern"))
    window.pattern = record.value("pattern")
    # logger.info("edit pat: " + str(window.pattern) + " - " + str(len(window.pattern)))
    if record.value("revolution") == 1:
        window.rb_1rev.setChecked(True)
    else:
        window.rb_2rev.setChecked(True)
    window.lineEdit_desc_curta.setText(record.value("short_desc"))
    window.lineEdit_desc_longa.setText(record.value("long_desc"))
    window.lineEdit_edges.setText(str(record.value("edges")))
    window.append_text_ptd_datetime("new: " + record.value("name"))



def btnw_insert(window):
    try:
        window.append_text_ptd_datetime("insert")
        query = QSqlQuery()
        query.prepare("INSERT INTO WheelPattern (name, pattern, edges, rpmscaler) VALUES (:name, :pattern, :edges, :rpmscaler"
                      ")")
        scaller = float(float(window.lineEdit_dentes.text()) / 120.0)
        scaller = float("{:.2f}".format(scaller))
        query.bindValue(":name", window.lineEdit_name.text())
        query.bindValue(":edges", window.lineEdit_dentes.text())
        query.bindValue(":rpmscaler", scaller)
        query.bindValue(":pattern", window.textEdit_pattern.toPlainText())
        query.exec_()
        window.lineEdit_name.setEnabled(False)
        window.lineEdit_dentes.setEnabled(False)
        window.textEdit_pattern.setEnabled(False)
        window.rb_1rev.setEnabled(False)
        window.rb_2rev.setEnabled(False)
        window.lineEdit_desc_curta.setEnabled(False)
        window.lineEdit_desc_longa.setEnabled(False)
        window.flag_new = False

    except Exception as e:
        logger.info("Error update " + str(e))
        # logger.info("Connected " + str(dig))


def btnw_edit(window):
    window.append_text_ptd_datetime("edit")
    window.lineEdit_name.setEnabled(True)
    window.lineEdit_dentes.setEnabled(True)
    window.rb_1rev.setEnabled(True)
    window.rb_2rev.setEnabled(True)
    window.lineEdit_desc_curta.setEnabled(True)
    window.lineEdit_desc_longa.setEnabled(True)


def cp_pattern(window):
    window.rb_1rev.setEnabled(False)
    window.rb_2rev.setEnabled(False)
    window.lineEdit_dentes.setEnabled(False)
    teeth = int(window.lineEdit_dentes.text())
    if window.flag_new:
        start_pat(window, teeth)
    else:
        edit_pat(window, teeth, window.pattern)
    window.btn_cp_pattern.setEnabled(False)
    window.tab_bar.setCurrentIndex(2)

    # window.textEdit_pattern.setText(window.textEdit_gen_pattern.toPlainText())


def btnw_update(window):
    try:
        if window.var1.debug:
            logger.info('update')
        record = window.modelWheel.record(window.tableWheel.currentIndex().row())
        prov_id = int(record.value("id"))
        window.append_text_ptd_datetime\
            ("update: " + str(record.value("id")))
        query = QSqlQuery()
        if window.var1.debug:
            logger.info('update 1')
        # query.prepare("UPDATE WheelPattern SET name = :name, pattern = :pattern,"
        #               " edges = :edges, rpmscaller = :rpmscaller WHERE id = :id ");
        #query.prepare(("UPDATE WheelPattern SET name = :name, pattern = :pattern, edges = :edges WHERE id = ") + str(prov_id));
        query.prepare(
            ("UPDATE WheelPattern SET name = :name, pattern = :pattern, teeth = :teeth, rpmscaler = :rpmscaler,"
             " short_desc = :short_desc, long_desc = :long_desc,  edges = :edges, "
             " revolution = :revolution WHERE id = ") + str(prov_id));
        edges = 0
        rev = 0
        if window.rb_1rev.isChecked():
            edges = int(int(window.lineEdit_dentes.text()) * 1 * 2)
            logger.info("rb1 ")
            rev = 1
            logger.info(query.lastError())
        else:
            edges = int(int(window.lineEdit_dentes.text()) * 2 * 2)
            logger.info("rb2 ")
            rev = 2
            logger.info(query.lastError())
        rpm_scaller = float(float(window.lineEdit_dentes.text())/120.0)
        rpm_scaller = float("{:.2f}".format(rpm_scaller))
        query.bindValue(":name", window.lineEdit_name.text())
        query.bindValue(":short_desc", window.lineEdit_desc_curta.text())
        query.bindValue(":long_desc", window.lineEdit_desc_longa.text())
        query.bindValue(":teeth", int(window.lineEdit_dentes.text()))
        query.bindValue(":rpmscaler", rpm_scaller)
        query.bindValue(":edges", edges)
        query.bindValue(":revolution", rev)
        query.bindValue(":pattern", window.textEdit_pattern.toPlainText())

        if window.var1.debug:
            logger.info('update 2')
            logger.info('update 2 :' + str(rpm_scaller) + " - " + str(edges))
            logger.info(query.lastError())
        query.bindValue(":id ", prov_id)
        query.exec_()
        if window.var1.debug:
            logger.info("update "+str(record.value("id"))+ " - " + str(prov_id))
            logger.info(query.lastError())
        window.tableWheel.update()
        if window.var1.debug:
            logger.info("update "+str(record.value("id"))+ " - " + str(prov_id))
            logger.info(query.lastError())
        window.lineEdit_name.setEnabled(False)
        window.lineEdit_dentes.setEnabled(False)
        window.textEdit_pattern.setEnabled(False)
        window.rb_1rev.setEnabled(False)
        window.rb_2rev.setEnabled(False)
        window.lineEdit_desc_curta.setEnabled(False)
        window.lineEdit_desc_longa.setEnabled(False)
    except Exception as e:
        logger.info("Error update " + str(e))
        # logger.info("Connected " + str(dig))


def tableChoose_clicked_db(window):

    if window.var1.debug:
        logger.info('tableWheel_clicked_db')
        window.append_text_ptd_datetime("tableChoose_clicked_db")
    record = window.modelChoose.record(window.tableWheel.currentIndex().row())

def btnw_cancel(window):
    window.append_text_ptd_datetime("cancel")
    window.lineEdit_name.setEnabled(False)
    window.lineEdit_dentes.setEnabled(False)
    window.textEdit_pattern.setEnabled(False)
    window.rb_1rev.setEnabled(False)
    window.rb_2rev.setEnabled(False)
    window.lineEdit_desc_curta.setEnabled(False)
    window.lineEdit_desc_longa.setEnabled(False)
    window.flag_new = False


def btnw_delete(window):
    window.append_text_ptd_datetime("delete")


def btnw_new(window):
    window.append_text_ptd_datetime("new")
    window.lineEdit_name.setText("")
    window.lineEdit_dentes.setText("")
    window.textEdit_pattern.setText("")
    window.lineEdit_name.setEnabled(True)
    window.lineEdit_dentes.setEnabled(True)
    window.rb_1rev.setEnabled(True)
    window.rb_2rev.setEnabled(True)
    window.lineEdit_desc_curta.setEnabled(True)
    window.lineEdit_desc_longa.setEnabled(True)
    window.flag_new = True
