CREATE TRIGGER SaleTrigger
    BEFORE INSERT ON Purchases
        FOR EACH ROW
    BEGIN
        SET @discount = 0.0;
        SET @product = (SELECT ProductId FROM Purchases 
            WHERE CustomerId = new.CustomerId AND ProductId = new.ProductId LIMIT 1);
        IF @product IS NOT NULL THEN
            SET @discount = @discount + 0.1;
        END IF;
        
        SET @avgprice = (SELECT AVG(Price) FROM Purchases WHERE ProductId = new.ProductId);
        IF @avgprice < new.Price THEN
            SET @discount = @discount + 0.05;
        END IF;
        
        IF @discount > 0 THEN
            SET new.Price = new.Price * (1 - @discount); 
        END IF;
    END;

INSERT INTO Purchases VALUES (9994, 97, 10, 3000);
INSERT INTO Purchases VALUES (9995, 98, 19, 4000);
INSERT INTO Purchases VALUES (9996, 98, 20, 7000);
INSERT INTO Purchases VALUES (9997, 99, 20, 5000);
INSERT INTO Purchases VALUES (9998, 99, 19, 3000);
INSERT INTO Purchases VALUES (9999, 99, 20, 8000);