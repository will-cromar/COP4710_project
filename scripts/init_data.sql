INSERT INTO Locations(lname, latitude, longitude) VALUES ('UCF Center', 28.6012, -81.2011);
INSERT INTO Universities(uname, primarylid, pop, descr) 
    VALUES ('UCF', 1, 65000, 'University of Central Florida');
INSERT INTO Universities(uname, primarylid, pop, descr) 
    VALUES ('UW', 1, 46000, 'University of Washington');

INSERT INTO Users VALUES ('admin', 'admin');
INSERT INTO SuperUsers VALUES ('admin');

INSERT INTO Users VALUES ('user1', 'password');
INSERT INTO Users VALUES ('user2', 'password');
INSERT INTO Users VALUES ('user3', 'password');
INSERT INTO Users VALUES ('user4', 'password');
INSERT INTO Users VALUES ('user5', 'password');
INSERT INTO Users VALUES ('user6', 'password');
INSERT INTO Users VALUES ('user7', 'password');
INSERT INTO Users VALUES ('user8', 'password');
INSERT INTO Users VALUES ('user9', 'password');
INSERT INTO Users VALUES ('user10', 'password');
INSERT INTO Users VALUES ('user11', 'password');
INSERT INTO Users VALUES ('user12', 'password');
INSERT INTO Users VALUES ('user13', 'password');
INSERT INTO Users VALUES ('user14', 'password');
INSERT INTO Users VALUES ('user15', 'password');
INSERT INTO Users VALUES ('user16', 'password');
INSERT INTO Users VALUES ('user17', 'password');
INSERT INTO Users VALUES ('user18', 'password');
INSERT INTO Users VALUES ('user19', 'password');
INSERT INTO Students(username, univid, email) VALUES ('user1', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user2', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user3', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user4', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user5', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user6', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user7', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user8', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user9', 1, 'someone@fake.ucf.edu');
INSERT INTO Students(username, univid, email) VALUES ('user10', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user11', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user12', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user13', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user14', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user15', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user16', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user17', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user18', 2, 'someone@fake.uw.edu');
INSERT INTO Students(username, univid, email) VALUES ('user19', 2, 'someone@fake.uw.edu');

INSERT INTO RSOs(rsoname, univid) VALUES ("COP 4710", 1);
INSERT INTO Admins VALUES ('user1', 1);
INSERT INTO RSOMembers VALUES ('user1', 1);
INSERT INTO RSOMembers VALUES ('user2', 1);
INSERT INTO RSOMembers VALUES ('user3', 1);
INSERT INTO RSOMembers VALUES ('user4', 1);
INSERT INTO RSOMembers VALUES ('user5', 1);


INSERT INTO RSOs(rsoname, univid) VALUES ("International Relations Club", 1);
INSERT INTO Admins VALUES ('user6', 2);
INSERT INTO RSOMembers VALUES ('user6', 2);
INSERT INTO RSOMembers VALUES ('user7', 2);
INSERT INTO RSOMembers VALUES ('user8', 2);
INSERT INTO RSOMembers VALUES ('user9', 2);

INSERT INTO RSOs(rsoname, univid) VALUES ("Theatre UCF", 2);
INSERT INTO Admins VALUES ('user11', 3);
INSERT INTO RSOMembers VALUES ('user11', 3);
INSERT INTO RSOMembers VALUES ('user12', 3);
INSERT INTO RSOMembers VALUES ('user13', 3);
INSERT INTO RSOMembers VALUES ('user14', 3);
INSERT INTO RSOMembers VALUES ('user15', 3);

INSERT INTO Events(title, lid, approved) VALUES ("Public Event", 1, 1);
INSERT INTO Events(title, urestriction, lid, approved) VALUES ("UCF Private Event", 1, 1, 1);
INSERT INTO Events(title, urestriction, lid, approved) VALUES ("UW Private Event", 2, 1, 1);
INSERT INTO Events(title, rsorestriction, lid, approved) VALUES ("COP 4710 Test Event", 1, 1, 1);
INSERT INTO Events(title, rsorestriction, lid, approved) VALUES ("IRC Test Event", 2, 1, 1);
INSERT INTO Events(title, rsorestriction, lid, approved) VALUES ("Theatre UCF Test Event", 3, 1, 1);
