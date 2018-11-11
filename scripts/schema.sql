CREATE TABLE Users(
    username VARCHAR(32),
    passwd VARCHAR(32),
    PRIMARY KEY (username)
);

CREATE TABLE SuperUsers(
    username VARCHAR(32),
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES Users(username)
        ON DELETE CASCADE
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
    primarylid INT,
    pop INT,
    descr TEXT,
    PRIMARY KEY (univid),
    FOREIGN KEY (primarylid) REFERENCES Locations(lid)
);

CREATE TABLE Students(
    username VARCHAR(32),
    univid INT NOT NULL,
    email VARCHAR(64),
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES Users(username)
        ON DELETE CASCADE,
    FOREIGN KEY (univid) REFERENCES Universities(univid)
);

CREATE TABLE RSOs(
    rid INT NOT NULL AUTO_INCREMENT,
    rsoname VARCHAR(64) UNIQUE,
    univid INT,
    approved BOOL DEFAULT 0,
    PRIMARY KEY (rid),
    FOREIGN KEY (univid) REFERENCES Universities(univid)
        ON DELETE CASCADE
);

CREATE TABLE Admins(
    username VARCHAR(32),
    rid INT,
    PRIMARY KEY (username, rid),
    FOREIGN KEY (username) REFERENCES Students(username)
        ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES RSOs(rid)
        ON DELETE CASCADE
);

CREATE TABLE Events(
    eid INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(64),
    descr TEXT,
    category VARCHAR(64),
    dtime DATETIME,
    lid INT,
    cphone CHAR(10),
    cemail VARCHAR(64),
    urestriction INT,
    rsorestriction INT,
    approved BOOL DEFAULT 0,
    PRIMARY KEY (eid),
    FOREIGN KEY (lid) REFERENCES Locations(lid),
    FOREIGN KEY (urestriction) REFERENCES Universities(univid)
        ON DELETE CASCADE,
    FOREIGN KEY (rsorestriction) REFERENCES RSOs(rid)
        ON DELETE CASCADE
);

CREATE TABLE RSOMembers(
    username VARCHAR(32),
    rid INT,
    PRIMARY KEY (username, rid),
    FOREIGN KEY (username) REFERENCES Students(username)
        ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES RSOs(rid)
        ON DELETE CASCADE
);

CREATE TABLE UserRating(
    username VARCHAR(32),
    eid INT,
    rating INT,
    PRIMARY KEY (username, eid),
    FOREIGN KEY (username) REFERENCES Users(username)
        ON DELETE CASCADE,
    FOREIGN KEY (eid) REFERENCES Events(eid)
        ON DELETE CASCADE
);

CREATE TABLE UserComment(
    cid INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(32),
    eid INT,
    comment TEXT,
    PRIMARY KEY (cid),
    FOREIGN KEY (username) REFERENCES Users(username)
        ON DELETE CASCADE,
    FOREIGN KEY (eid) REFERENCES Events(eid)
        ON DELETE CASCADE
);

CREATE TABLE Photos(
    pid INT NOT NULL AUTO_INCREMENT,
    univid INT,
    b64 MEDIUMTEXT NOT NULL,
    ftype VARCHAR(16),
    PRIMARY KEY (pid),
    FOREIGN KEY (univid) REFERENCES Universities(univid)
        ON DELETE CASCADE
);
