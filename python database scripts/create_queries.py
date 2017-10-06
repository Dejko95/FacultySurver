# -*- coding: utf-8 -*-

TABLES = {}

TABLES['semestar'] = ("CREATE TABLE `semestar` (\
 `id_semestra` int(11) NOT NULL AUTO_INCREMENT,\
 `školska_godina` varchar(10) COLLATE utf8_unicode_ci NOT NULL,\
 `broj_semestra` int(11) NOT NULL,\
 `tip_semestra` varchar(10) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_semestra`),\
 UNIQUE KEY `školska_godina` (`školska_godina`,`broj_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['trenutni_semestar'] = ("CREATE TABLE `trenutni_semestar` (\
 `id_trenutnog_semestra` int(11) NOT NULL AUTO_INCREMENT,\
 `školska_godina` varchar(10) COLLATE utf8_unicode_ci NOT NULL,\
 `tip_semestra` varchar(10) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_trenutnog_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT")

TABLES['student'] = ("CREATE TABLE `student` (\
 `id_studenta` int(11) NOT NULL AUTO_INCREMENT,\
 `ime` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `prezime` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `indeks` varchar(20) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_studenta`)\
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['studentski_nalog'] = ("CREATE TABLE `studentski_nalog` (\
 `id` int(11) NOT NULL AUTO_INCREMENT,\
 `id_studenta` int(11) NOT NULL,\
 `username` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `password` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id`)\
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['predmet'] = ("CREATE TABLE `predmet` (\
 `id_predmeta` int(11) NOT NULL AUTO_INCREMENT,\
 `naziv` varchar(60) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_predmeta`),\
 UNIQUE KEY `naziv` (`naziv`)\
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['grupa'] = ("CREATE TABLE `grupa` (\
 `id_grupe` int(11) NOT NULL AUTO_INCREMENT,\
 `broj` varchar(8) COLLATE utf8_unicode_ci NOT NULL,\
 `id_semestra` int(11) NOT NULL,\
 PRIMARY KEY (`id_grupe`),\
 UNIQUE KEY `broj` (`broj`,`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['nastavnik'] = ("CREATE TABLE `nastavnik` (\
 `id_nastavnika` int(11) NOT NULL AUTO_INCREMENT,\
 `ime` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `prezime` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `tip` varchar(20) COLLATE utf8_unicode_ci NOT NULL,\
 `email` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_nastavnika`),\
 UNIQUE KEY `ime` (`ime`,`prezime`,`tip`)\
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['drži_predmet'] = ("CREATE TABLE `drži_predmet` (\
 `id` int(11) NOT NULL AUTO_INCREMENT,\
 `id_nastavnika` int(11) NOT NULL,\
 `id_predmeta` int(11) NOT NULL,\
 `id_grupe` int(11) NOT NULL,\
 PRIMARY KEY (`id`),\
 UNIQUE KEY `id_nastavnika` (`id_nastavnika`,`id_predmeta`,`id_grupe`)\
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['pitanje'] = ("CREATE TABLE `pitanje` (\
 `id_pitanja` int(11) NOT NULL AUTO_INCREMENT,\
 `tekst` text COLLATE utf8_unicode_ci NOT NULL,\
 `tip` varchar(20) COLLATE utf8_unicode_ci NOT NULL,\
 `format` varchar(20) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_pitanja`)\
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['student_u_grupi'] = ("CREATE TABLE `student_u_grupi` (\
 `id` int(11) NOT NULL AUTO_INCREMENT,\
 `id_studenta` int(11) NOT NULL,\
 `id_grupe` int(11) NOT NULL,\
 PRIMARY KEY (`id`)\
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['odgovor_fakultet'] = ("CREATE TABLE `odgovor_fakultet` (\
 `id_odgovora` int(11) NOT NULL AUTO_INCREMENT,\
 `id_pitanja` int(11) NOT NULL,\
 `id_studenta` int(11) NOT NULL,\
 `id_semestra` int(11) NOT NULL,\
 `odgovor` text COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_odgovora`),\
 UNIQUE KEY `id_pitanja` (`id_pitanja`,`id_studenta`,`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['odgovor_predmet'] = ("CREATE TABLE `odgovor_predmet` (\
 `id_odgovora` int(11) NOT NULL AUTO_INCREMENT,\
 `id_pitanja` int(11) NOT NULL,\
 `id_studenta` int(11) NOT NULL,\
 `id_predmeta` int(11) NOT NULL,\
 `id_semestra` int(11) NOT NULL,\
 `odgovor` text COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_odgovora`),\
 UNIQUE KEY `id_pitanja_2` (`id_pitanja`,`id_studenta`,`id_predmeta`,`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['odgovor_nastavnik'] = ("CREATE TABLE `odgovor_nastavnik` (\
 `id_odgovora` int(11) NOT NULL AUTO_INCREMENT,\
 `id_pitanja` int(11) NOT NULL,\
 `id_studenta` int(11) NOT NULL,\
 `id_drži_predmet` int(11) NOT NULL,\
 `id_semestra` int(11) NOT NULL,\
 `odgovor` text COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_odgovora`),\
 UNIQUE KEY `id_pitanja_2` (`id_pitanja`,`id_studenta`,`id_drži_predmet`,`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT")
