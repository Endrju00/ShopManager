CREATE TABLE `adresy` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `miasto` varchar(100) NOT NULL,
  `ulica` varchar(100) NOT NULL,
  `nr_ulicy` int(10) unsigned NOT NULL CHECK (`nr_ulicy` >= 0),
  `kod_pocztowy` varchar(6) NOT NULL,
  `kraj` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Adresy_miasto_ulica_nr_ulicy_kod_pocztowy_kraj_7a07ae8d_uniq` (`miasto`,`ulica`,`nr_ulicy`,`kod_pocztowy`,`kraj`)
);

CREATE TABLE `dostarczone_towary` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `data` date NOT NULL,
  `ilosc` int(10) unsigned NOT NULL CHECK (`ilosc` >= 0),
  `cena_jednostkowa_zakupu` double NOT NULL,
  `cena_jednostkowa_sprzedazy` double NOT NULL,
  `kod_produktu` bigint(20) DEFAULT NULL,
  `hurtownia` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Dostarczone_towary_data_hurtownia_kod_produktu_093e3907_uniq` (`data`,`hurtownia`,`kod_produktu`),
  KEY `Dostarczone_towary_hurtownia_f783c2bb_fk_Hurtownie_id` (`hurtownia`),
  KEY `Dostarczone_towary_kod_produktu_0fc89a23_fk_Produkty_id` (`kod_produktu`),
  CONSTRAINT `Dostarczone_towary_hurtownia_f783c2bb_fk_Hurtownie_id` FOREIGN KEY (`hurtownia`) REFERENCES `hurtownie` (`id`) ON DELETE SET NULL,
  CONSTRAINT `Dostarczone_towary_kod_produktu_0fc89a23_fk_Produkty_id` FOREIGN KEY (`kod_produktu`) REFERENCES `produkty` (`id`) ON DELETE SET NULL
);

CREATE TABLE `hurtownie` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nazwa` (`nazwa`)
);

CREATE TABLE `kategorie` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(100) NOT NULL,
  `nadkategoria` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nazwa` (`nazwa`),
  KEY `Kategorie_nadkategoria_589c7fdc_fk_Kategorie_id` (`nadkategoria`),
  CONSTRAINT `Kategorie_nadkategoria_589c7fdc_fk_Kategorie_id` FOREIGN KEY (`nadkategoria`) REFERENCES `kategorie` (`id`) ON DELETE SET NULL
);

CREATE TABLE `klienci` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `imie` varchar(100) NOT NULL,
  `nazwisko` varchar(100) NOT NULL,
  `nr_telefonu` varchar(9) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `kod_karty_rabatowej` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `platnosci` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `data` datetime(6) NOT NULL,
  `kwota` double NOT NULL,
  `numer_zamowienia` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Platnosci_data_numer_zamowienia_ded19c93_uniq` (`data`,`numer_zamowienia`),
  KEY `Platnosci_numer_zamowienia_703a5a8d_fk_Zamowienia_numer` (`numer_zamowienia`),
  CONSTRAINT `Platnosci_numer_zamowienia_703a5a8d_fk_Zamowienia_numer` FOREIGN KEY (`numer_zamowienia`) REFERENCES `zamowienia` (`numer`) ON DELETE SET NULL
);

CREATE TABLE `pozycje_w_zamowieniach` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ilosc_zamawiana` int(10) unsigned NOT NULL CHECK (`ilosc_zamawiana` >= 0),
  `id_dostawy` bigint(20) DEFAULT NULL,
  `numer_zamowienia` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Pozycje_w_zamowieniach_id_dostawy_numer_zamowienia_849647b8_uniq` (`id_dostawy`,`numer_zamowienia`),
  KEY `Pozycje_w_zamowienia_numer_zamowienia_3635710a_fk_Zamowieni` (`numer_zamowienia`),
  CONSTRAINT `Pozycje_w_zamowienia_id_dostawy_ac70d56a_fk_Dostarczo` FOREIGN KEY (`id_dostawy`) REFERENCES `dostarczone_towary` (`id`) ON DELETE SET NULL,
  CONSTRAINT `Pozycje_w_zamowienia_numer_zamowienia_3635710a_fk_Zamowieni` FOREIGN KEY (`numer_zamowienia`) REFERENCES `zamowienia` (`numer`) ON DELETE CASCADE
);

CREATE TABLE `pracownicy` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `imie` varchar(100) NOT NULL,
  `nazwisko` varchar(100) NOT NULL,
  `nr_telefonu` varchar(9) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `placa` double NOT NULL,
  `ilosc_godzin_tyg` int(10) unsigned NOT NULL CHECK (`ilosc_godzin_tyg` >= 0),
  `nazwa_stanowiska` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Pracownicy_nazwa_stanowiska_9ec0aac8_fk_Stanowiska_id` (`nazwa_stanowiska`),
  CONSTRAINT `Pracownicy_nazwa_stanowiska_9ec0aac8_fk_Stanowiska_id` FOREIGN KEY (`nazwa_stanowiska`) REFERENCES `stanowiska` (`id`) ON DELETE SET NULL
);

CREATE TABLE `producenci` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(100) NOT NULL,
  `strona_www` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nazwa` (`nazwa`)
);

CREATE TABLE `produkty` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `kod` bigint(20) unsigned NOT NULL CHECK (`kod` >= 0),
  `nazwa` varchar(100) NOT NULL,
  `opis` longtext NOT NULL,
  `kategoria` bigint(20) DEFAULT NULL,
  `producent` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kod` (`kod`),
  KEY `Produkty_kategoria_d7f1206f_fk_Kategorie_id` (`kategoria`),
  KEY `Produkty_producent_34667843_fk_Producenci_id` (`producent`),
  CONSTRAINT `Produkty_kategoria_d7f1206f_fk_Kategorie_id` FOREIGN KEY (`kategoria`) REFERENCES `kategorie` (`id`) ON DELETE SET NULL,
  CONSTRAINT `Produkty_producent_34667843_fk_Producenci_id` FOREIGN KEY (`producent`) REFERENCES `producenci` (`id`) ON DELETE SET NULL
);

CREATE TABLE `stanowiska` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(100) NOT NULL,
  `placa_min` double NOT NULL,
  `placa_max` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nazwa` (`nazwa`)
);

CREATE TABLE `zamowienia` (
  `numer` int(11) NOT NULL AUTO_INCREMENT,
  `data_zlozenia` date NOT NULL,
  `status` varchar(100) NOT NULL,
  `komentarz` longtext DEFAULT NULL,
  `id_adresu` bigint(20) DEFAULT NULL,
  `id_klienta` bigint(20) DEFAULT NULL,
  `id_pracownika` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`numer`),
  KEY `Zamowienia_id_adresu_273d308d_fk_Adresy_id` (`id_adresu`),
  KEY `Zamowienia_id_klienta_143871d4_fk_Klienci_id` (`id_klienta`),
  KEY `Zamowienia_id_pracownika_33a9ddcd_fk_Pracownicy_id` (`id_pracownika`),
  CONSTRAINT `Zamowienia_id_adresu_273d308d_fk_Adresy_id` FOREIGN KEY (`id_adresu`) REFERENCES `adresy` (`id`) ON DELETE SET NULL,
  CONSTRAINT `Zamowienia_id_klienta_143871d4_fk_Klienci_id` FOREIGN KEY (`id_klienta`) REFERENCES `klienci` (`id`) ON DELETE SET NULL,
  CONSTRAINT `Zamowienia_id_pracownika_33a9ddcd_fk_Pracownicy_id` FOREIGN KEY (`id_pracownika`) REFERENCES `pracownicy` (`id`) ON DELETE SET NULL
);

delimiter //
create or replace procedure podwyzka(IN pId INTEGER, IN pPodwyzka FLOAT) 
    begin
    UPDATE pracownicy
    SET placa = placa + pPodwyzka
    WHERE id = pId; 
    end //

delimiter //
CREATE OR REPLACE FUNCTION CenaZamowienia (pNumerZamowienia INTEGER)
RETURNS FLOAT

BEGIN
    DECLARE vCena FLOAT;
    
    SELECT SUM(p.ilosc_zamawiana * d.cena_jednostkowa_sprzedazy)
    INTO vCena
    FROM zamowienia z JOIN pozycje_w_zamowieniach p
    ON z.numer=p.numer_zamowienia
    JOIN dostarczone_towary d ON p.id_dostawy=d.id
    WHERE z.numer=pNumerZamowienia
    GROUP BY z.numer;
    RETURN vCena;
END; //

DELIMITER ;