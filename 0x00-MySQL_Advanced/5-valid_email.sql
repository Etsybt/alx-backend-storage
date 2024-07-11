-- Check if the trigger exists
SELECT COUNT(*) INTO @trigger_exists
FROM INFORMATION_SCHEMA.TRIGGERS
WHERE TRIGGER_NAME = 'resets_valid_email'
  AND TRIGGER_SCHEMA = 'my_database_6';

-- If the trigger exists, drop it
IF @trigger_exists > 0 THEN
    DROP TRIGGER resets_valid_email;
END IF;

-- Create the trigger
DELIMITER //
CREATE TRIGGER resets_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END//
DELIMITER ;
