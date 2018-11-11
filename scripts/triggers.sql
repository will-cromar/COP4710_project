CREATE TRIGGER approverso
AFTER INSERT ON RSOMembers
FOR EACH ROW
UPDATE RSOs 
SET approved = (SELECT COUNT(*) > 4
                FROM RSOMembers R
                WHERE R.rid = rid)
WHERE RSOs.rid = rid;

CREATE TRIGGER unapproverso
AFTER DELETE ON RSOMembers
FOR EACH ROW
UPDATE RSOs 
SET approved = (SELECT COUNT(*) > 4
                FROM RSOMembers R
                WHERE R.rid = rid)
WHERE RSOs.rid = rid;



-- Enforce valid range of rating values [1, 5]
ALTER TABLE UserRating ADD CONSTRAINT CHECK (rating > 0 AND rating < 6);

-- Can't be both a private and an RSO event
ALTER TABLE Events ADD CONSTRAINT CHECK (urestriction = NULL or rsorestriction = NULL);

-- Prevent scheduling two events at the same time/place
ALTER TABLE Events ADD CONSTRAINT UNIQUE(dtime, lid);
