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