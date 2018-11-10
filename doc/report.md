---
title: "Group Report: University Events"
subtitle: "COP 4710 Group 32"
author: William Cromar
documentclass: scrartcl
geometry:
- left=1in
- right=1in
- top=1in
- bottom=1in

toc: true
numbersections: true
---

# Overview

The overall architecture of the project is extremely simple in order to lighten the workload, since I’m working on the project alone. The backend is designed as a monolithic web server written in Python with Flask and a MySQL database. The web frontend is almost all static (written with just HTML and CSS) content generated from the backend and displayed in the browser, although there are some frontend components written in JavaScript to support advanced features.

The database accessed from the backend server through the official MySQL connection library for Python, which safely templates queries. As such, almost all SQL is embedded in strings in the Python application, with the exception of initial startup scripts. There are a few scripts written in SQL (saved in `scripts/` directory) to initialize the database schema and populate with some basic test data. These are expected to be run once by the administrator before starting the web server for the first time.

Figure \ref{architecture} shows an overview of the application's architecture.

![Overview of application's architecture \label{architecture}](doc/img/overview.png){width=50%}

# Database

## Design

The relational model used for the database is shown in Figure \ref{er_diagram}. Most of the design of the data model flowed naturally from the requirements of the project, but there are a few key areas where trade-offs had to be analyzed and important design decisions had to be made. These decisions are covered in the following sections.

![ER Model for events website. \label{er_diagram}](doc/img/er_diagram.png)

There are multiple valid ways to design the database, and my final design reflects my own personal experiences and preferences in software engineering. In order to better demonstrate why I made the decisions and trade-offs that I did, I provide an outline of my design philosophy:

1. Design the database schema to be easy to mutate without introducing anomalies.
1. Write views to make querying the database easier for the client when following (1) makes the data harder to read.
1. Don’t take (1) to an extreme: views should be simple, understandable, and easy to update for schema changes.

### Event

There are three event types given in the project requirements: public, private, and RSO events. Nearly all attributes of the events are common across all three types.These arguably form an inheritance hierarchy, where there’s a supertype Event and three subtypes that add attributes. There are three conventional ways to implement such a hierarchy:

1. Store each type of event in its own separate table. This makes querying all events significantly more difficult.
1. Store all three types in the same table, and only use some attributes for certain types of events. This imposes a risk of setting conflicting options (i.e. making an event that’s both RSO and private type), but makes querying all events quite easy.
1. Store all common attributes in one main table Events and have tables for each type that reference it. This makes querying common attributes of events easy, but make determining the scope of an event given just its common attributes harder.

A separate decision to display the scope of an event in the user interface informed a decision to select option (2). In this design, all events are assumed to be public unless the set either a _university restriction_ or _rso restriction_. In order to mitigate the risk of erroneously creating an event that sets both restrictions, a simple check was introduced to the table to ensure only zero or one restriction is set (see Section \ref{constraints}). Then, the scope of an event can be determine just by querying the one table.

### Users

A similar decision is required to accurately represent the three user types: student, admin, and super-admin. A slightly different approach is taken to solve it, though:

1. Anyone can sign up for a username and password and are added to the `Users` table.
1. A user can be promoted to super admin by the DBA, who can add their name directly to the `SuperUsers` table.
1. `Users` can enter their university name and student e-mail to become a _student_ in the Students table.
1. A student can request to create an RSO, and will be added to the Admins table. Note that this design permits multiple admins for one RSO and allows a student to administer multiple RSOs. This new RSO is approved by a super admin.

The information in these tables is combined into one view, that has the users credentials, nullable student information, and a flag indicating whether they are a _super admin_.

### Location

The location of an event can either be stored separately in some table, or all of that information can be embedded in both Events and Universities. I chose the former option to facilitate easier location selection, where a user can create an event by choosing the name of the location from a list rather than having to select off of a map every time. However, an interactive map is still available to add new location entries (see Section \ref{interactive_map}).

### Other Decisions

A number of other minor design decisions are listed here:

- The range of a rating (1 to 5) is enforced by a CHECK constraint.
- RSOs have an approved field, and only move to the `ApprovedRSOs` view when the _SuperAdmin_ presses the “Approved” button.
- Images of universities can be uploaded by super admins, which are encoded as base 64 in the database.
- A student seeking to create an RSO must provide the names of 5 other students at the time of creation in the interface.
- All ID values that act as primary keys are auto-incremented integers.

## Relational Schema

The following is the contents of `schema.sql`, which is used to define the tables needed for the application.

\VerbatimInput{scripts/schema.sql}

### Views

The following is the contents of `views.sql`, which defines several views used by the application for convenience.

\VerbatimInput{scripts/views.sql}

## Constraints

The following sections demonstrate the constraints that could not be expressed as simple key constraints. The demonstrations of these constraints do not contain a full set of test data, in order to make the constraints easier to understand in isolation.

### Range of User Ratings

A simple `CHECK` is used to enforce the range of user ratings (1 to 5). This is also enforced by the GUI, which does not allow ratings outside of this range.

```SQL
ALTER TABLE UserRating ADD CONSTRAINT CHECK (rating > 0 AND rating < 6);
```

### Overlapping Event Times/Locations

A `UNIQUE` constraint is used to ensure that no two events are scheduled at the same time at the same place. See Figure \ref{fig_overlap} for a demonstration.

```SQL
ALTER TABLE Events ADD CONSTRAINT UNIQUE(dtime, lid);
```

![Attempting to insert two events at the same place and time fails, but two events at the same time and different places is allowed \label{fig_overlap}](doc/img/overlapping_event.png)

### Disabling RSOs with Fewer than 5 Members

Two `TRIGGER` constraints are used to activate RSOs with enough members and deactivate those the too few members. See Figure \ref{fig_trigger} for a demonstration.

```SQL
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
```

![The RSO is activated when the fifth member is added and deactivated when he/she is removed. \label{fig_trigger}](doc/img/rso_triggers.png)

### Non-admin Creating RSO Events

This constraint is enforced by the application rather than the database. The GUI presents a list containing only the current user's RSOs and Universities to restrict the scope of the event. So, a non-admin can't create an event on behalf of an RSO. See Figure \ref{restriction_list} for an example.

![The current user does not administer any RSOs, so they cannot create an RSO event, but they can request to create a private event for their university. \label{restriction_list}](doc/img/restriction_list.png)

## Example Queries

In this section, I provide some examples of embedded queries from the backend application that demonstrate how the database is used in practice. The string `%s` indicates that the backend application will populate that field based on the current application state.

### Fetch All RSO Events

```SQL
SELECT * FROM ApprovedEvents
WHERE rsorestriction IN (
    SELECT rid FROM RSOMembers
    WHERE username = %s);
```

This query gets all events that have been created for an approved RSO where the current user has membership in that RSO. The design of the representation of Events lends itself to convenient querying of Events and filtering by access restrictions.

### Create a New Location

```SQL
INSERT INTO Locations(lname, latitude, longitude)
VALUES (%s, %s, %s)
```

Although the database enforces the uniqueness of location names, it automatically determines a unique primary key that identifies the location in the rest of the database. Representing locations in a separate tables allows the client to easy query (for example) all events at some location:

```SQL
SELECT *
FROM ApprovedEvents
WHERE lid = %s;
```

### Update and Access University Photo Albums

More detail on the visual design of this element is provided in Section \ref{university_album}.

```SQL
INSERT INTO Photos(univid, b64, ftype)
VALUES (%s, %s, %s)
```

This query adds an uploaded photo (converted to base 64) to an album for a specific university. It is equally easy to fetch an entire album from the application:

```SQL
SELECT *
FROM Photos
WHERE univid=%s;
```

# Graphical User Interface

The following series of figures demonstrate a typical path through the application from a new user's perspective.

![A new user starts on the home page of the application.](doc/img/home_page.png)

![The new user registers with a username (`will`) and password.](doc/img/make_account.png)

![The user selects their school and university e-mail address.](doc/img/student_info.png)

![Any student can request to create an event private to their university. Note that the form also has client-side input validation.](doc/img/event_form.png)

![Once a super-admin approved the private event, the user can see it in their list of events](doc/img/small_event_list.png)

![The user can click "View" to see all of the details of the event, as well as leave a comment](doc/img/event_details.png)

![Users also have the option to edit their comments.](doc/img/event_comment.png)

![The new user can request to create an RSO with 5 of their friends and will become that RSO's first admin](doc/img/new_rso.png)

![Now that the user is an admin of an RSO, they can create an RSO event for it.](doc/img/rso_event.png)

# Non-essential Features

The central part of the project is the database, and the backend application provides a thin layer that lets users securely access it. In this section, I describe features that go beyond the minimum requirements to make the database functional and accessible and make it easier to use the application.

## Interface Design

I went out of my way to may the website intuitive and visually appealing. Some screenshots are provided below.

screenshots

## UCF Event Feed Scraping

A Python script is included in the `scripts/` directory that fetches a week worth of events from the official UCF events website and generate the `INSERT` statements to adapt the data to my database design. This can be used to populate the database with real test data.

## Social Networking

All event details pages include an option to share the event on Twitter.

screenshot

## Interactive Maps {#interactive_map}
Event details pages all feature an interactive map that lets users see the area around where an event is scheduled. Additionally, new events can be created by selecting the name of an existing location from a list, but users can also add new locations to host their event at using an interactive map.

screenshots

## University Album {#university_album}


