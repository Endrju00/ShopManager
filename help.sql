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
	
	SELECT SUM(p.ilosc_zamawiana * d.cena_jednostkowa_zakupu)
	INTO vCena
	FROM zamowienia z JOIN pozycje_w_zamowieniach p
	ON z.numer=p.numer_zamowienia
	JOIN dostarczone_towary d ON p.id_dostawy=d.id
	WHERE z.numer=pNumerZamowienia
	GROUP BY z.numer;
	RETURN vCena;
END; //

DELIMITER ;