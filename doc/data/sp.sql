DELIMITER &&
CREATE PROCEDURE Compute_Ratings()
BEGIN
    DECLARE done int default 0;
    DECLARE currRoomID INT;
    DECLARE currResCount INT;
    DECLARE currBuildingID INT;
    DECLARE currRegion VARCHAR(255);
    DECLARE maxCountInRegion INT;
    DECLARE newRating REAL;
    DECLARE newPopularity REAL;
    DECLARE currStarRating VARCHAR(5);
    DECLARE cur CURSOR FOR SELECT RoomID, ResCount, BuildingID, Region FROM (SELECT RoomID, COUNT(RoomID) as ResCount FROM reservation GROUP BY RoomID) tmp NATURAL JOIN room NATURAL JOIN building;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    DROP TABLE IF EXISTS star_ratings;
    CREATE TABLE star_ratings (
        RoomID INT PRIMARY KEY,
        StarRating VARCHAR(5),
        Region VARCHAR(255) NOT NULL
    );
    OPEN cur;
    REPEAT
        FETCH cur INTO currRoomID, currResCount, currBuildingID, currRegion;
        SET maxCountInRegion = (SELECT MAX(ResCount) FROM (SELECT RoomID, COUNT(RoomID) AS ResCount FROM reservation GROUP BY RoomID) tmp NATURAL JOIN room NATURAL JOIN building b WHERE b.Region = currRegion);
        SET newRating = (currResCount / maxCountInRegion) * 100;
        SET newPopularity = 50.0 + ((currResCount / maxCountInRegion) * 50);
        UPDATE room SET Popularity=newPopularity WHERE RoomID=currRoomID;
        IF (newRating >= 80) THEN 
            SET currStarRating = '*****';
        ELSEIF (newRating >= 60) THEN
            SET currStarRating = '****';
        ELSEIF (newRating >= 40) THEN
            SET currStarRating = '***';
        ELSEIF (newRating >= 20) THEN
            SET currStarRating = '**';
        ELSE
            SET currStarRating = '*';
        END IF;
        INSERT IGNORE star_ratings VALUES (currRoomID, currStarRating, currRegion);
    UNTIL done
    END REPEAT;
    SELECT * FROM star_ratings s ORDER BY CHAR_LENGTH(s.StarRating) DESC, s.Region, s.RoomID;
END &&
DELIMITER ;