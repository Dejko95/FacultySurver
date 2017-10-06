# -*- coding: utf-8 -*-
from __future__ import print_function

import mysql.connector

DB_NAME = 'raf_anketa5'

cnx = mysql.connector.connect(user='root', password='', host='localhost', charset='utf8')
cursor = cnx.cursor()


def create_database():
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

