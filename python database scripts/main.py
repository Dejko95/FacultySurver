# -*- coding: utf-8 -*-
from __future__ import print_function
from database import *
from create_queries import TABLES
from mysql.connector import errorcode
from timetable_parser import import_timetable_data
from insert_queries import INSERTS
from questions import import_questions

#kreiranje baze, ili povezivanje na postojecu ako postoji
try:
    cnx.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database()
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


#kreiranje tabela
for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
cnx.commit()


#ubacivanje semestra u bazu
try:
    cursor.execute(INSERTS['trenutni_semestar'])
    cursor.execute(INSERTS['semestar'])
except mysql.connector.Error as err:
    print(err)


#parsiranje rasporeda
import_timetable_data()


#ubacivanje podataka o studentima
try:
    cursor.execute(INSERTS['student'])
    cursor.execute(INSERTS['studentski_nalog'])
    cursor.execute(INSERTS['student_u_grupi'])
except mysql.connector.Error as err:
    print(err)

#ubacivanje pitanja
import_questions()

cnx.commit()
#zatvaranje konekcije
cursor.close()
cnx.close()