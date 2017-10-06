# -*- coding: utf-8 -*-
from database import *
from getters import get_current_semestar

cnx.database = DB_NAME
trenutni_semestar = get_current_semestar(cursor)


def get_total_count():
    query = "SELECT count(DISTINCT svi.id_studenta) "\
            "FROM ((SELECT DISTINCT id_studenta FROM odgovor_fakultet "\
                  " JOIN semestar ON odgovor_fakultet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s) "\
                  " UNION ALL "\
                  "(SELECT DISTINCT id_studenta FROM odgovor_nastavnik "\
                  " JOIN semestar ON odgovor_nastavnik.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s) "\
                  " UNION ALL "\
                  "(SELECT DISTINCT id_studenta FROM odgovor_predmet "\
                  " JOIN semestar ON odgovor_predmet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s) "\
                  ") "\
                  "AS svi"

    cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"],
                           trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"],
                           trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"]))
    for (count, ) in cursor:
        return count


def get_count_per_year(godina):
    if trenutni_semestar["tip_semestra"] == 'zimski':
        query_broj_semestra = godina * 2 - 1
    else:
        query_broj_semestra = godina * 2

    query = "SELECT count(DISTINCT svi.id_studenta) " \
            "FROM ((SELECT DISTINCT id_studenta FROM odgovor_fakultet " \
            " JOIN semestar ON odgovor_fakultet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s AND semestar.broj_semestra = %s) " \
            " UNION ALL " \
            "(SELECT DISTINCT id_studenta FROM odgovor_nastavnik " \
            " JOIN semestar ON odgovor_nastavnik.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s AND semestar.broj_semestra = %s) " \
            " UNION ALL " \
            "(SELECT DISTINCT id_studenta FROM odgovor_predmet " \
            " JOIN semestar ON odgovor_predmet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s AND semestar.broj_semestra = %s) " \
            ") " \
            "AS svi"

    cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], query_broj_semestra,
                           trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], query_broj_semestra,
                           trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], query_broj_semestra))
    for (count,) in cursor:
        return count


def get_faculty_questions_reports():
    query = "SELECT id_pitanja, tekst FROM pitanje WHERE tip='fakultet' AND format='ocena'"
    cursor.execute(query)
    pitanja = []
    for (id_pitanja, tekst) in cursor:
        pitanja.append((id_pitanja, tekst))

    izvestaj_global = {}
    for (id_pitanja, tekst) in pitanja:
        broj_glasova = [0, 0, 0, 0, 0, 0]
        for opcija in range(1, 6):
            query = "SELECT COUNT(*) FROM odgovor_fakultet "\
                    "JOIN semestar ON odgovor_fakultet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s "\
                    "AND semestar.tip_semestra = %s AND id_pitanja = %s AND odgovor_fakultet.odgovor = %s"
            cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], id_pitanja, opcija))
            for (count, ) in cursor:
                broj_glasova[opcija] = count
        suma = sum(broj_glasova)
        izvestaj = {}
        for opcija in range(1,6):
            izvestaj[opcija] = {"broj_glasova": broj_glasova[opcija],
                                "procenat": broj_glasova[opcija] * 100 / float(suma)}
        izvestaj_global[tekst] = izvestaj

    return izvestaj_global


def get_teacher_reports():
    query = "SELECT * FROM predmet"
    cursor.execute(query)
    predmeti = []
    for (id_predmeta, naziv) in cursor:
        predmeti.append((id_predmeta, naziv))
    izvestaj_global = {}
    for (id_predmeta, naziv_predmeta) in predmeti:
        # svi profesori koji drze ovaj predmet
        query = "SELECT DISTINCT nastavnik.id_nastavnika, nastavnik.ime, nastavnik.prezime FROM drži_predmet " \
                "JOIN nastavnik ON drži_predmet.id_nastavnika = nastavnik.id_nastavnika AND drži_predmet.id_predmeta = %s " \
                "JOIN grupa ON drži_predmet.id_grupe = grupa.id_grupe " \
                "JOIN semestar ON grupa.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s "
        cursor.execute(query, (id_predmeta, trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"]))
        nastavnici = []
        for (id_nastavnika, ime, prezime) in cursor:
            nastavnici.append((id_nastavnika, ime, prezime))
        # print(naziv_predmeta)
        # print(nastavnici)
        # broj studenata koji su ocenili ovaj predmet
        query = "SELECT COUNT(DISTINCT odgovor_predmet.id_studenta) FROM odgovor_predmet " \
                "JOIN semestar ON odgovor_predmet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND " \
                "semestar.tip_semestra = %s AND odgovor_predmet.id_predmeta = %s "
        cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], id_predmeta))
        broj_studenata_predmeta = 0
        for (count,) in cursor:
            broj_studenata_predmeta = count

        # prosecna ocena predmeta
        query = "SELECT AVG(odgovor_predmet.odgovor) FROM odgovor_predmet " \
                "JOIN semestar ON odgovor_predmet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s AND odgovor_predmet.id_predmeta = %s " \
                "JOIN pitanje ON odgovor_predmet.id_pitanja = pitanje.id_pitanja AND pitanje.format = 'ocena'"
        cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], id_predmeta))
        prosecna_ocena_predmeta = 0
        for (avg,) in cursor:
            prosecna_ocena_predmeta = avg

        prosecne_ocene_nastavnika = []
        for (id_nastavnika, ime, prezime) in nastavnici:
            # prosecna ocena nastavnika na ovom predmetu
            query = "SELECT AVG(odgovor_nastavnik.odgovor) FROM odgovor_nastavnik " \
                    "JOIN semestar ON odgovor_nastavnik.id_semestra = semestar.id_semestra AND " \
                    "semestar.školska_godina = %s AND semestar.tip_semestra = %s " \
                    "JOIN drži_predmet ON odgovor_nastavnik.id_drži_predmet = drži_predmet.id AND drži_predmet.id_nastavnika = %s " \
                    "AND drži_predmet.id_predmeta = %s " \
                    "JOIN pitanje ON odgovor_nastavnik.id_pitanja = pitanje.id_pitanja AND pitanje.format = 'ocena' "
            cursor.execute(query, (
            trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], id_nastavnika, id_predmeta))
            for (avg,) in cursor:
                prosecna_ocena_nastavnika = avg

            izvestaj_global[(naziv_predmeta, ime, prezime)] = prosecna_ocena_nastavnika

    return izvestaj_global


def get_subjects_marks():
    query = "SELECT * FROM predmet"
    cursor.execute(query)
    predmeti = []
    for (id_predmeta, naziv) in cursor:
        predmeti.append((id_predmeta, naziv))

    izvestaj_global = {}
    for (id_predmeta, naziv) in predmeti:
        query = "SELECT AVG(odgovor_predmet.odgovor) FROM odgovor_predmet "\
                "JOIN semestar ON odgovor_predmet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s AND odgovor_predmet.id_predmeta = %s "\
                "JOIN pitanje ON odgovor_predmet.id_pitanja = pitanje.id_pitanja AND pitanje.format = 'ocena'"
        cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], id_predmeta))
        for (avg,) in cursor:
            izvestaj_global[naziv] = avg
    return izvestaj_global


def get_teacher_per_course_reports():
    query = "SELECT * FROM predmet"
    cursor.execute(query)
    predmeti = []
    for (id_predmeta, naziv) in cursor:
        predmeti.append((id_predmeta, naziv))

    izvestaj_global = {}
    for (id_predmeta, naziv_predmeta) in predmeti:
        #svi profesori koji drze ovaj predmet
        query = "SELECT DISTINCT nastavnik.id_nastavnika, nastavnik.ime, nastavnik.prezime FROM drži_predmet "\
                "JOIN nastavnik ON drži_predmet.id_nastavnika = nastavnik.id_nastavnika AND drži_predmet.id_predmeta = %s "\
                "JOIN grupa ON drži_predmet.id_grupe = grupa.id_grupe "\
                "JOIN semestar ON grupa.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s "
        cursor.execute(query, (id_predmeta, trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"]))
        nastavnici = []
        for (id_nastavnika, ime, prezime) in cursor:
            nastavnici.append((id_nastavnika, ime, prezime))

        # broj studenata koji su ocenili ovaj predmet
        query = "SELECT COUNT(DISTINCT odgovor_predmet.id_studenta) FROM odgovor_predmet " \
                "JOIN semestar ON odgovor_predmet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND " \
                "semestar.tip_semestra = %s AND odgovor_predmet.id_predmeta = %s "
        cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], id_predmeta))
        broj_studenata_predmeta = 0
        for (count,) in cursor:
            broj_studenata_predmeta = count

        # prosecna ocena predmeta
        query = "SELECT AVG(odgovor_predmet.odgovor) FROM odgovor_predmet "\
                "JOIN semestar ON odgovor_predmet.id_semestra = semestar.id_semestra AND semestar.školska_godina = %s AND semestar.tip_semestra = %s AND odgovor_predmet.id_predmeta = %s "\
                "JOIN pitanje ON odgovor_predmet.id_pitanja = pitanje.id_pitanja AND pitanje.format = 'ocena'"
        cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], id_predmeta))
        prosecna_ocena_predmeta = 0
        for (avg,) in cursor:
            prosecna_ocena_predmeta = avg

        prosecne_ocene_nastavnika = []
        for (id_nastavnika, ime, prezime) in nastavnici:
            #prosecna ocena nastavnika na ovom predmetu
            query = "SELECT AVG(odgovor_nastavnik.odgovor) FROM odgovor_nastavnik "\
                    "JOIN semestar ON odgovor_nastavnik.id_semestra = semestar.id_semestra AND "\
                    "semestar.školska_godina = %s AND semestar.tip_semestra = %s "\
                    "JOIN drži_predmet ON odgovor_nastavnik.id_drži_predmet = drži_predmet.id AND drži_predmet.id_nastavnika = %s " \
                    "AND drži_predmet.id_predmeta = %s "\
                    "JOIN pitanje ON odgovor_nastavnik.id_pitanja = pitanje.id_pitanja AND pitanje.format = 'ocena' "
            cursor.execute(query, (trenutni_semestar["skolska_godina"], trenutni_semestar["tip_semestra"], id_nastavnika, id_predmeta))
            for (avg,) in cursor:
                prosecne_ocene_nastavnika.append((ime + " " + prezime, avg))

        for (id_nastavnika, ime, prezime) in nastavnici:
            izvestaj_global[(naziv_predmeta, id_nastavnika)] = {"broj_studenata": broj_studenata_predmeta,
                                                               "prosecna_ocena_predmeta": prosecna_ocena_predmeta,
                                                               "ocene_nastavnika": prosecne_ocene_nastavnika}

    return izvestaj_global


def get_all_teachers():
    query = "SELECT id_nastavnika, ime, prezime, email FROM nastavnik WHERE tip='Profesor'"
    cursor.execute(query)
    nastavnici = []
    for (id_nastavnika, ime, prezime, email) in cursor:
        nastavnici.append((id_nastavnika, ime, prezime, email))
    return nastavnici
