"""
Version: 0a
Tecnocoli - @11/2021
Author: Jeferson Coli - jcoli@tecnocoli.com.br
Digital Simulator
Main
"""

# import hashlib


class Variables:
    # Connection
    bit_alive = True
    thread_bit = False
    mil_lamp = True
    conected = False
    livebit_tmp = 0
    thread_flag = None
    debug = True
    conn_timeout = 20
    flag_new = False
    value_serial = ""
    thread_flag = None
    conn_timeout = 20
    flag_new = False

    # System
    debug = True
    prog_id = []

    # flags I/O
    stopGo = False
    next_rpm = 0
    inject_live = False
    L50 = False
    L30 = False
    L15 = False
    oute_01 = False
    port_a = 0
    port_c = 0
    port_d = 0
    port_e = 0
    port_f = 0
    port_g = 0
    port_h = 0
    port_l = 0
    port_k = 0

    port_z = 0
    port_y = 0
    port_x = 0

    in_a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
    # in_k = [0, 0, 0, 0, 0, 0, 0, 0]
    ana_out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ana_inp = [0, 0, 0, 0, 0, 0, 0, 0]
    oute_c = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    # oute_l = [0, 0, 0, 0, 0, 0, 0, 0]

    inj1 = False;
    inj1_show = False
    inj2 = False;
    inj2_show = False
    inj3 = False;
    inj3_show = False
    inj4 = False;
    inj4_show = False
    coil1 = False
    coil1_show = False
    coil2 = False
    coil2_show = False
    coil3 = False
    coil3_show = False
    coil4 = False
    coil4_show = False
    # rpm_min = 0
    # rpm_max = 7500
    # hash_id = hashlib.md5()
    # inTx = False
    # inRx = False
    # edges = 0
    # max_pages = 13
    # edges_last_page = 10
    # page_pattern = 1
    # pattern_p = ""
    # pattern_pt = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    # pattern = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
