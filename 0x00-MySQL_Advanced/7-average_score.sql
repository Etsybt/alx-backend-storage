-- Define a delimiter for the stored procedure
DELIMITER $$

-- Remove the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser $$

-- Create the stored procedure ComputeAverageScoreForUser
CREATE PROCEDURE ComputeAverageScoreForUser(IN p_user_id INT)
BEGIN
    -- Update the user's average score by calculating the average score from the corrections table
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE corrections.user_id = p_user_id
    )
    WHERE id = p_user_id;
END $$

-- Reset the delimiter back to the default
DELIMITER ;
