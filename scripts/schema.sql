CREATE TABLE Users(
    username VARCHAR(32),
    passwd VARCHAR(32),
    PRIMARY KEY (username)
);

CREATE TABLE SuperUsers(
    username VARCHAR(32),
    PRIMARY KEY (username)
);

CREATE TABLE Locations(
    lid INT NOT NULL AUTO_INCREMENT,
    lname VARCHAR(64),
    latitude FLOAT,
    longitude FLOAT,
    PRIMARY KEY (lid)
);

CREATE TABLE Universities(
    univid INT NOT NULL AUTO_INCREMENT,
    uname VARCHAR(64),
    lid INT,
    descr TEXT,
    PRIMARY KEY (univid),
    FOREIGN KEY (lid) REFERENCES Locations(lid)
);

CREATE TABLE Students(
    username VARCHAR(32),
    univid INT,
    email VARCHAR(64),
    PRIMARY KEY (username),
    FOREIGN KEY (univid) REFERENCES Universities(univid)
);

CREATE TABLE RSOs(
    rid INT NOT NULL AUTO_INCREMENT,
    rsoname VARCHAR(64),
    PRIMARY KEY (rid)
);

CREATE TABLE Admins(
    username VARCHAR(32),
    rid INT,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES Students(username),
    FOREIGN KEY (rid) REFERENCES RSOs(rid)
);

CREATE TABLE Events(
    eid INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(64),
    dtime DATETIME,
    lid INT,
    cphone CHAR(10),
    cemail VARCHAR(64),
    urestriction INT,
    rsorestriction INT,
    PRIMARY KEY (eid),
    FOREIGN KEY (lid) REFERENCES Locations(lid),
    FOREIGN KEY (urestriction) REFERENCES Universities(univid),
    FOREIGN KEY (rsorestriction) REFERENCES RSOs(rid),

    -- Can't be both a private and an RSO event
    CHECK (urestriction = NULL or rsorestriction = NULL)
);

CREATE TABLE RSOMembers(
    username VARCHAR(32),
    rid INT,
    PRIMARY KEY (username, rid),
    FOREIGN KEY (username) REFERENCES Students(username),
    FOREIGN KEY (rid) REFERENCES RSOs(rid)
);

CREATE TABLE UserRating(
    username VARCHAR(32),
    eid INT,
    rating INT,
    PRIMARY KEY (username, eid),
    FOREIGN KEY (username) REFERENCES Users(username),
    FOREIGN KEY (eid) REFERENCES Events(eid),

    -- 1 to 5 star rating
    CHECK (rating > 0 AND rating > 1)
);

CREATE TABLE UserComment(
    cid INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(32),
    eid INT,
    comment TEXT,
    PRIMARY KEY (cid),
    FOREIGN KEY (username) REFERENCES Users(username),
    FOREIGN KEY (eid) REFERENCES Events(eid)
);