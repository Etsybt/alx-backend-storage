-- Drop the function if it already exists
DROP FUNCTION IF EXISTS SafeDiv;

-- Create the SafeDiv function
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    DECLARE result FLOAT;

    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = a / b;
    END IF;

    RETURN result;
END $$

DELIMITER ;
