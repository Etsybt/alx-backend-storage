DELIMITER $$

CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if project exists or create if it doesn't
    SELECT id INTO project_id FROM projects WHERE name = p_project_name;
    
    IF project_id IS NULL THEN
        -- Project doesn't exist, create a new project
        INSERT INTO projects (name) VALUES (p_project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the new correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (p_user_id, project_id, p_score);
END$$

DELIMITER ;
