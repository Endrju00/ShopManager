delimiter //
create or replace procedure podwyzka(IN pId INTEGER, IN pPodwyzka FLOAT) 
	begin
	UPDATE employees_employee
	SET salary = salary + pPodwyzka
	WHERE id = pId; 
	end //

delimiter //
CREATE OR REPLACE FUNCTION CenaZamowienia (pNumerZamowienia INTEGER)
RETURNS FLOAT

BEGIN
	DECLARE vCena FLOAT;
	
	SELECT SUM(p.quantity * d.unit_selling_price)
	INTO vCena
	FROM orders_order z JOIN orders_iteminorder p
	ON z.id=p.order_id
	JOIN products_delivereditems d ON p.delivery_id=d.id
	WHERE z.id=pNumerZamowienia
	GROUP BY z.id;
	RETURN vCena;
END; //

DELIMITER ;