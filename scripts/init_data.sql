INSERT INTO Locations(lname, latitude, longitude) VALUES ('UCF Center', 28.6012, -81.2011);
INSERT INTO Universities(uname, primarylid, pop, descr) 
    VALUES ('UCF', 1, 65000, 'University of Central Florida');

INSERT INTO Users VALUES ('admin', 'admin');
INSERT INTO SuperUsers VALUES ('admin');
INSERT INTO Users VALUES ('user1', 'password');
INSERT INTO Students(username, univid, email) VALUES ('user1', 1, 'someone@fake.ucf.edu');
INSERT INTO Users VALUES ('user2', 'password');
INSERT INTO Students(username, univid, email) VALUES ('user2', 1, 'someone@fake.ucf.edu');
INSERT INTO Users VALUES ('user3', 'password');
INSERT INTO Students(username, univid, email) VALUES ('user3', 1, 'someone@fake.ucf.edu');
INSERT INTO Users VALUES ('user4', 'password');
INSERT INTO Students(username, univid, email) VALUES ('user4', 1, 'someone@fake.ucf.edu');
INSERT INTO Users VALUES ('user5', 'password');
INSERT INTO Students(username, univid, email) VALUES ('user5', 1, 'someone@fake.ucf.edu');
INSERT INTO Users VALUES ('user6', 'password');
INSERT INTO Students(username, univid, email) VALUES ('user6', 1, 'someone@fake.ucf.edu');
