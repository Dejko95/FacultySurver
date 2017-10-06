# -*- coding: utf-8 -*-
from database import cursor
from insert_queries import INSERTS
import mysql.connector

def import_questions():
    with open("pitanja.txt", "r") as pitanja:
        for line in pitanja:
            lista = line.split(";")
            tekst = lista[0]
            tip = lista[1]
            format = lista[2]

            pitanje_data = (tekst, tip, format)
            try:
                cursor.execute(INSERTS['pitanje'], pitanje_data)
            except mysql.connector.Error as err:
                #print(err)
                pass