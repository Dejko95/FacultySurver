# -*- coding: utf-8 -*-
import report_queries
from database import *
from mail_sender import sendMail


def faculty_reports():
    with open("izvestaj_fakultet.txt", "w+") as fajl:
        fajl.write("Ukupan broj studenata koji se popunili anketu: " + str(report_queries.get_total_count()) + "\n")
        fajl.write("\n")
        for godina in range(1,5):
            fajl.write("Broj studenata na " + str(godina) + "-oj godini koji su popunili anketu: " + str(report_queries.get_count_per_year(godina)) + "\n")
        fajl.write("\n")
        fajl.write("Statistika pitanja:\n")
        pitanja = report_queries.get_faculty_questions_reports()
        for tekst_pitanja, ocene in pitanja.iteritems():
            pass
            fajl.write(tekst_pitanja.encode("utf-8") + "\n")
            for ocena in range(1,6):
                fajl.write("\t" + str(ocena) + ": ")
                fajl.write(str(ocene[ocena]['broj_glasova']) + " glasova ")
                fajl.write("(" + str(ocene[ocena]['procenat']) + "%)\n")
        fajl.write("\n")
        fajl.write("Prosečne ocene predmeta:\n")
        predmeti = report_queries.get_subjects_marks()
        for predmet, ocena in predmeti.iteritems():
            fajl.write("* " + predmet.encode('utf8') + ": " + str(ocena) + "\n")
            #print(predmet + ": " + str(ocena) + "\n")
        fajl.write("\n")
        fajl.write("Prosečne ocene nastavnika po predmetima:\n")
        nastavnici = report_queries.get_teacher_reports()
        print(nastavnici)
        for (predmet, ime, prezime), ocena in nastavnici.iteritems():
            fajl.write("* " + (ime + " " + prezime).encode('utf8') + " na predmetu " + predmet.encode('utf8') + ": " + str(ocena) + "\n")


def teachers_reports():
    nastavnici = report_queries.get_all_teachers()
    print(nastavnici)

    izvestaj = report_queries.get_teacher_per_course_reports()
    #for (predmet, id_nastavnika1), ocene in izvestaj.iteritems():
    #    print(predmet + " " + str(id_nastavnika1))
    for (id_nastavnika, ime, prezime, email) in nastavnici:
        if email.endswith('test'):
            continue
        #print(ime + " " + prezime)
        counter = 0
        for (predmet, id_nastavnika1), ocene in izvestaj.iteritems():
            if id_nastavnika != id_nastavnika1:
                continue
            #print(ime + " " + prezime + " " + predmet)
            lista_fajlova = []
            counter += 1
            ime_fajla = 'nastavnicki_izvestaji/izvestaj' + str(id_nastavnika) + "_" + str(counter) + ".txt"
            with open(ime_fajla, "w+") as fajl:
                fajl.write("Predmet: " + predmet + "\n\n")
                fajl.write("-Broj anketiranih studenata za predmet: " + str(ocene['broj_studenata']) + "\n")
                fajl.write("-Prosečna ocena predmeta: " + str(ocene['prosecna_ocena_predmeta']) + "\n\n")
                fajl.write("*Prosečne ocene predavača na predmetu:" + "\n")
                for (nastavnik, ocena) in ocene['ocene_nastavnika']:
                    fajl.write("  " + nastavnik.encode('utf8') + ": " + str(ocena) + "\n")
                lista_fajlova.append(ime_fajla)
            print(lista_fajlova)
            if (len(lista_fajlova) > 0):
                sendMail([email], 'Izveštaj ankete na Računarskom fakultetu za ' + ime.encode("utf-8") + prezime.encode("utf-8"), 'U prilogu se nalazi izveštaj za svaki od predmeta koje držite', lista_fajlova)

faculty_reports()
teachers_reports()

cursor.close()
cnx.close()