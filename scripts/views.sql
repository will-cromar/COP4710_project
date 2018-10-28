CREATE VIEW EasyUsers AS
SELECT Users.*, Students.univid, Students.email,
    Users.username IN (SELECT * FROM SuperUsers) AS super
FROM Users
LEFT JOIN Students ON Users.username = Students.username;

CREATE VIEW ApprovedRSOs AS
SELECT RSOs.*, Universities.uname
FROM RSOs JOIN Universities
ON RSOs.univid = Universities.univid
WHERE approved = 1;

CREATE VIEW EventsInfo AS 
SELECT Events.*, Universities.uname, RSOs.rsoname,
    Locations.lname, Locations.latitude, Locations.longitude
FROM Events
JOIN Locations ON Events.lid = Locations.lid
LEFT JOIN RSOs ON Events.rsorestriction = RSOs.rid
LEFT JOIN Universities ON Events.urestriction = Universities.univid
ORDER BY eid;

CREATE VIEW ApprovedEvents AS
SELECT * FROM EventsInfo
WHERE approved = 1;
