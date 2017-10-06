# -*- coding: utf-8 -*-
from __future__ import print_function
import mysql.connector
from insert_queries import INSERTS
from getters import *
from database import *

def import_timetable_data():
    ADDED_COURSES = set()
    ADDED_TEACHERS = set()
    ADDED_GROUPS = set()

    trenutni_semestar = get_current_semestar(cursor)

    with open("csv", "r") as raspored:
        next(raspored)
        line_number = 1
        for line in raspored:
            print(line_number)
            line_number += 1
            row = line[1:-1].split('","')
            #print(row)

            # for i in range(len(row)):
            #     row[i] = row[i][1:-1]       #sklanjanje navodnika

            predmet = row[0]
            tip_casa = row[1]
            if (tip_casa == 'Predavanja'):
                tip = 'Profesor'
            elif (tip_casa == 'Vezbe'):
                tip = 'Asistent'
            elif (tip_casa == 'Laboratorijske vezbe'):
                tip = 'Saradnik'
            nastavnik = row[2]
            poz = nastavnik.rfind(" ")
            prezime = nastavnik[:poz]
            ime = nastavnik[poz+1:]
            email = ime.lower() + prezime.lower() + "@test.test"
            grupe = row[3]
            grupe_lista = [x.strip() for x in grupe.split(",")]

            predmet_data = (predmet, )
            if not (predmet_data in ADDED_COURSES):
                try:
                    cursor.execute(INSERTS['predmet'], predmet_data)
                    ADDED_COURSES.add(predmet_data)
                except mysql.connector.Error as err:
                    #print(err)
                    pass

            nastavnik_data = (ime, prezime, tip, email)
            if not (nastavnik_data in ADDED_TEACHERS):
                try:
                    cursor.execute(INSERTS['nastavnik'], nastavnik_data)
                    ADDED_TEACHERS.add(nastavnik_data)
                except mysql.connector.Error as err:
                    #print(err)
                    pass
            #print(grupe)
            #print(grupe_lista)

            id_nastavnika = get_teacher_id(cursor, ime, prezime, tip)
            id_predmeta = get_course_id(cursor, predmet)
            #print(predmet, id_predmeta)

            for grupa in grupe_lista:
                #print(grupa)

                id_semestra = get_semestar_id(cursor, grupa, trenutni_semestar)

                grupa_data = (grupa, id_semestra)
                if not (grupa_data in ADDED_GROUPS):
                    try:
                        cursor.execute(INSERTS['grupa'], grupa_data)
                        cnx.commit()
                        ADDED_GROUPS.add(grupa_data)
                    except mysql.connector.Error as err:
                        #print(err)
                        pass
                    for i in range(10000000):
                        pass
                id_grupe = get_group_id(cursor, grupa, trenutni_semestar)
                #print(id_grupe)

                drzi_predmet_data = (id_nastavnika, id_predmeta, id_grupe)
                try:
                    cursor.execute(INSERTS['drzi_predmet'], drzi_predmet_data)
                except mysql.connector.Error as err:
                    #print(err)
                    pass


# trenutni_semestar = get_current_semestar(cursor)
# print(trenutni_semestar)
# id_grupe = get_group_id(cursor, '307', trenutni_semestar)
# id_semestra = get_semestar_id(cursor, '3s2', trenutni_semestar)
# print(id_semestra)
# get_teacher_id(cursor, 'Stancic', 'Aleksandar', 'Asistent')
# get_course_id(cursor, 'Istorija racunarstva')
