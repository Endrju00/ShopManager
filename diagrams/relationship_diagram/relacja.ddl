create table Pracownicy(
    id NUMERIC(10) GENERATED ALWAYS AS IDENTITY primary key,
    imie VARCHAR(100) not null,
    nazwisko VARCHAR(100) not null,
    nr_telefonu CHAR(9) not null,
    email VARCHAR(100),
    placa NUMERIC(10, 2) not null,
    ilosc_godzin_tyg NUMERIC(10) not null,
    nazwa_stanowiska VARCHAR(100) references Stanowiska(nazwa) not null 
);

create table Stanowiska(
    nazwa VARCHAR(100) GENERATED ALWAYS AS IDENTITY primary key,
    placa_min NUMERIC(10, 2) not null,
    placa_max NUMERIC(10, 2) not null
);

create table Klienci(
    id NUMERIC(10) GENERATED ALWAYS AS IDENTITY primary key,
    imie VARCHAR(100) not null,
    nazwisko VARCHAR(100) not null,
    nr_telefonu CHAR(9) not null,
    email VARCHAR(100),
    kod_karty_rabatowej VARCHAR(100)
);

create table Adresy(
    id NUMERIC(10) GENERATED ALWAYS AS IDENTITY primary key,
    miasto VARCHAR(100) not null,
    ulica VARCHAR(100) not null,
    nr_ulicy VARCHAR(100) not null,
    kod_pocztowy CHAR(6) not null,
    kraj VARCHAR(100) not null,
    UNIQUE(miasto, ulica, nr_ulicy, kod_pocztowy, kraj)
);

create table Zamowienia(
    numer NUMERIC(10) primary key,
    data_zlozenia DATE not null,
    status VARCHAR(100) not null,
    komentarz VARCHAR(1000),
    id_pracownika NUMERIC(10) references Pracownicy(id) not null,
    id_klienta NUMERIC(10) references Klienci(id) not null,
    id_adresu NUMERIC(10) references Adresy(id) not null
);

create table Platnosci(
    id NUMERIC(10) GENERATED ALWAYS AS IDENTITY primary key,
    data DATE not null,
    kwota NUMERIC(10, 2) not null,
    numer_zamowienia NUMERIC(10) references Zamowienia(numer) not null,
    primary key(id),
    UNIQUE(data, numer_zamowienia)
);

create table Produkty(
    kod NUMERIC(10) primary key,
    nazwa VARCHAR(100) not null,
    opis VARCHAR(1000),
    producent VARCHAR(100) references Producenci(nazwa) not null,
    kategoria VARCHAR(100) references Kategorie(nazwa) not null
);

create table Producenci(
    nazwa VARCHAR(100) primary key,
    strona_www VARCHAR(100)
);

create table Kategorie(
    nazwa VARCHAR(100) primary key,
    nadkategoria VARCHAR(100) references Kategorie(nazwa) null
);

create table Hurtownie(
    nazwa VARCHAR(100) primary key
);

create table Dostarczone_towary(
    id NUMERIC(10) GENERATED ALWAYS AS IDENTITY primary key,
    data DATE not null,
    ilosc NUMERIC(10) not null,
    cena_jednostkowa_zakupu NUMERIC(10, 2) not null,
    cena_jednostkowa_sprzedazy NUMERIC(10, 2) not null,
    kod_produktu NUMERIC(10) references Produkty(kod) not null,
    hurtownia VARCHAR(100) references Hurtownie(nazwa) not null,
    UNIQUE(data, kod_produktu, hurtownia)
);

create table Pozycje_w_zamowieniach(
    id NUMERIC(10) GENERATED ALWAYS AS IDENTITY primary key,
    ilosc_zamawiana NUMERIC(10) not null,
    id_dostawy NUMERIC(10) references Dostarczone_towary(id) not null,
    numer_zamowienia NUMERIC(10) references Zamowienia(numer) not null,
    primary key(id),
    UNIQUE(numer_zamowienia, id_dostawy)
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
