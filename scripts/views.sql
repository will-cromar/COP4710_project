CREATE VIEW EasyUsers AS
SELECT Users.*, Students.univid, Students.email,
    Users.username IN (SELECT * FROM SuperUsers) AS super
FROM Users
LEFT JOIN Students ON Users.username = Students.username;

CREATE VIEW PublicEvents AS
SELECT *
FROM Events
WHERE approved = 1 AND
    urestriction IS NULL AND
    rsorestriction IS NULL;

CREATE VIEW PrivateEvents AS
SELECT *
FROM Events
WHERE approved = 1 AND
    urestriction IS NOT NULL;

CREATE VIEW RSOEvents AS
SELECT *
FROM Events
WHERE approved = 1 AND
    rsorestriction IS NOT NULL;