CREATE TABLE adresy (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  miasto varchar(100) NOT NULL,
  ulica varchar(100) NOT NULL,
  nr_ulicy int(10) unsigned NOT NULL CHECK (nr_ulicy >= 0),
  kod_pocztowy varchar(6) NOT NULL,
  kraj varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY Adresy_UK (miasto,ulica,nr_ulicy,kod_pocztowy, kraj)
);

CREATE TABLE producenci (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  nazwa varchar(100) NOT NULL,
  strona_www varchar(100) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY producenci_UK (nazwa)
);

CREATE TABLE hurtownie (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  nazwa varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY hurtownie_UK (nazwa)
);

CREATE TABLE kategorie (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  nazwa varchar(100) NOT NULL,
  id_nadkategorii bigint(20) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY kategorie_UK (nazwa),
  CONSTRAINT kategorie_FK FOREIGN KEY (id_nadkategorii) REFERENCES kategorie (id) ON DELETE SET NULL
);

CREATE TABLE klienci (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  imie varchar(100) NOT NULL,
  nazwisko varchar(100) NOT NULL,
  nr_telefonu varchar(9) NOT NULL,
  email varchar(254) DEFAULT NULL,
  kod_karty_rabatowej varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE stanowiska (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  nazwa varchar(100) NOT NULL,
  placa_min double NOT NULL,
  placa_max double NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY stanowiska_UK (nazwa)
);

CREATE TABLE pracownicy (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  imie varchar(100) NOT NULL,
  nazwisko varchar(100) NOT NULL,
  nr_telefonu varchar(9) NOT NULL,
  email varchar(254) DEFAULT NULL,
  placa double NOT NULL,
  ilosc_godzin_tyg int(10) unsigned NOT NULL CHECK (ilosc_godzin_tyg >= 0),
  id_stanowiska bigint(20) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT Pracownicy_nazwa_stanowiska_FK FOREIGN KEY (id_stanowiska) REFERENCES stanowiska (id)
);

CREATE TABLE produkty (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  kod bigint(20) unsigned NOT NULL CHECK (kod >= 0),
  nazwa varchar(100) NOT NULL,
  opis longtext DEFAULT NULL,
  id_kategorii bigint(20) NOT NULL,
  id_producenta bigint(20) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY produkty_UK (kod),
  CONSTRAINT Produkty_kategoria_FK FOREIGN KEY (id_kategorii) REFERENCES kategorie (id),
  CONSTRAINT Produkty_producent_FK FOREIGN KEY (id_producenta) REFERENCES producenci (id)
);

CREATE TABLE dostarczone_towary (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  data date NOT NULL,
  ilosc int(10) unsigned NOT NULL CHECK (ilosc >= 0),
  cena_jednostkowa_zakupu double NOT NULL,
  cena_jednostkowa_sprzedazy double NOT NULL,
  id_produktu bigint(20) NOT NULL,
  id_hurtownii bigint(20) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY Dostarczone_towary_UK (data,id_hurtownii,id_produktu),
  CONSTRAINT Dostarczone_towary_hurtownia_FK FOREIGN KEY (id_hurtownii) REFERENCES hurtownie (id),
  CONSTRAINT Dostarczone_towary_kod_produktu_FK FOREIGN KEY (id_produktu) REFERENCES produkty (id)
);

CREATE TABLE zamowienia (
  numer int(11) NOT NULL AUTO_INCREMENT,
  data_zlozenia date NOT NULL,
  status varchar(100) NOT NULL,
  komentarz longtext DEFAULT NULL,
  id_adresu bigint(20) NOT NULL,
  id_klienta bigint(20) NOT NULL,
  id_pracownika bigint(20) NOT NULL,
  PRIMARY KEY (numer),
  CONSTRAINT Zamowienia_id_adresu_FK FOREIGN KEY (id_adresu) REFERENCES adresy (id),
  CONSTRAINT Zamowienia_id_klienta_FK FOREIGN KEY (id_klienta) REFERENCES klienci (id),
  CONSTRAINT Zamowienia_id_pracownika_FK FOREIGN KEY (id_pracownika) REFERENCES pracownicy (id)
);

CREATE TABLE pozycje_w_zamowieniach (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  ilosc_zamawiana int(10) unsigned NOT NULL CHECK (ilosc_zamawiana >= 0),
  id_dostawy bigint(20) NOT NULL,
  numer_zamowienia int(11) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY Pozycje_w_zamowieniach_UK (id_dostawy,numer_zamowienia),
  CONSTRAINT Pozycje_w_zamowienia_id_dostawy_FK FOREIGN KEY (id_dostawy) REFERENCES dostarczone_towary (id),
  CONSTRAINT Pozycje_w_zamowienia_numer_zamowienia_FK FOREIGN KEY (numer_zamowienia) REFERENCES zamowienia (numer) ON DELETE CASCADE
);

CREATE TABLE platnosci (
  id bigint(20) NOT NULL AUTO_INCREMENT,
  data datetime(6) NOT NULL,
  kwota double NOT NULL,
  numer_zamowienia int(11) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY Platnosci_UK (data,numer_zamowienia),
  CONSTRAINT Platnosci_numer_zamowienia_FK FOREIGN KEY (numer_zamowienia) REFERENCES zamowienia (numer)
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