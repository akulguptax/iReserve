SELECT * FROM building b NATURAL JOIN room r
WHERE NOT EXISTS (SELECT * FROM reservation res WHERE r.RoomID = res.RoomID AND res.StartTime = "2022-04-26 15:00:00")
ORDER BY Popularity DESC;


CREATE TRIGGER UpdateRatingTrigger
    AFTER INSERT ON reservation FOR EACH ROW
    BEGIN
        SET @popularity = (SELECT r.Popularity FROM room r WHERE r.RoomID = new.RoomID LIMIT 1);
        IF @popularity <= 80 THEN
            SET @popularity = @popularity + 1;
            UPDATE room SET Popularity = @popularity WHERE RoomID = new.RoomID;
        END IF;
    END;



SELECT * FROM (reservation r WHERE r.GroupID IN (SELECT GroupID FROM groupassignment WHERE UserID = 677) AND r.UserID != 677) tmp 
    NATURAL JOIN room NATURAL JOIN building NATURAL JOIN `group` ORDER BY tmp.StartTime DESC;


SELECT tmp.num_res, COUNT(*) FROM (SELECT UserID, COUNT(*) AS num_res FROM reservation GROUP BY UserID) tmp GROUP BY tmp.num_res ORDER BY tmp.num_res DESC;

