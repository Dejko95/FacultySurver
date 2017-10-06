# -*- coding: utf-8 -*-`

INSERTS = {}

#Dinamicki inserti
INSERTS['nastavnik'] = ("INSERT INTO nastavnik "
                        "(ime, prezime, tip, email) "
                        "VALUES (%s, %s, %s, %s)")

INSERTS['predmet'] = ("INSERT INTO predmet "
                      "(naziv) "
                      "VALUES (%s)")

INSERTS['grupa'] = ("INSERT INTO grupa "
                    "(broj, id_semestra) "
                    "VALUES (%s, %s)")

INSERTS['drzi_predmet'] =("INSERT INTO drži_predmet "
                          "(id_nastavnika, id_predmeta, id_grupe) "
                          "VALUES (%s, %s, %s)")

INSERTS['pitanje'] = ("INSERT INTO pitanje "
                      "(tekst, tip, format) "
                      "VALUES (%s, %s, %s)")


#Staticki podaci
INSERTS['trenutni_semestar'] = ("INSERT INTO `trenutni_semestar` (`školska_godina`, `tip_semestra`) VALUES "
                                "('2016/2017', 'letnji')")

INSERTS['semestar'] = ("INSERT INTO `semestar` (`školska_godina`, `broj_semestra`, `tip_semestra`) VALUES"
                       "('2016/2017', 1, 'zimski'),"
                       "('2016/2017', 2, 'letnji'),"
                       "('2016/2017', 3, 'zimski'),"
                       "('2016/2017', 4, 'letnji'),"
                       "('2016/2017', 5, 'zimski'),"
                       "('2016/2017', 6, 'letnji'),"
                       "('2016/2017', 7, 'zimski'),"
                       "('2016/2017', 8, 'letnji'),"
                       "('2015/2016', 1, 'letnji'),"
                       "('2015/2016', 2, 'letnji'),"
                       "('2015/2016', 3, 'zimski'),"
                       "('2015/2016', 4, 'letnji'),"
                       "('2015/2016', 5, 'zimski'),"
                       "('2015/2016', 6, 'letnji'),"
                       "('2015/2016', 7, 'zimski'),"
                       "('2015/2016', 8, 'letnji'),"
                       "('2016/2017', -2, 'letnji'),"
                       "('2016/2017', -1, 'zimski')")


INSERTS['student'] = ("INSERT INTO `student` (`id_studenta`, `ime`, `prezime`, `indeks`) VALUES"
                      "(1, 'Ivan', 'Dejković', 'RN-16/2016'),"
                      "(2, 'Marko', 'Marković', 'RM-14/2016'),"
                      "(3, 'Nikola', 'Nikolić', 'RN-77/2016')")


INSERTS['studentski_nalog'] = ("INSERT INTO `studentski_nalog` (`id_studenta`, `username`, `password`) VALUES"
                               "(1, 'ivan', 'ivan'),"
                               "(2, 'marko', 'marko'),"
                               "(3, 'nikola', 'nikola');")


INSERTS['student_u_grupi'] = ("INSERT INTO `student_u_grupi` (`id_studenta`, `id_grupe`) VALUES "
                              "('1', '33'),"
                              "('2', '6'),"
                              "('3', '7');")

