/* select priority users: in a CS 400 level or has 7+ reservations */
(SELECT DISTINCT u.FirstName, u.LastName
 FROM `user` u NATURAL JOIN `groupassignment` ga NATURAL JOIN `group` grp
 WHERE grp.GroupName LIKE 'CS4__ %'
)
UNION
(SELECT u.FirstName, u.LastName FROM `user` u
 WHERE u.UserID IN (SELECT r.UserID 
                    FROM reservation r 
                    GROUP BY r.UserID 
                    HAVING COUNT(r.UserID) >= 7)
);

SELECT tmp.BuildingName, AVG(tmp.Popularity) AS AVG_POPULARITY
FROM (SELECT * FROM room r NATURAL JOIN building b
WHERE r.RoomID IN (SELECT res.RoomID FROM reservation res WHERE res.StartTime LIKE "2021-05%")) AS tmp
GROUP BY tmp.BuildingName
HAVING AVG(tmp.Popularity) > 50
ORDER BY AVG_POPULARITY DESC;
