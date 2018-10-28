import datetime
import json

import requests

raw = requests.get("https://events.ucf.edu/this-week/feed.json")
data = json.loads(raw.text)
loc_set = set(row["location"] for row in data)

for loc in loc_set:
    print("INSERT Locations(lname, latitude, longitude) VALUES('%s', 28.6012, -81.2011);" % loc)

for row in data:
    row["dtime"] = datetime.datetime.strptime(
        row["starts"], "%a, %d %b %Y %X %z").strftime(
            "%Y-%m-%d %X"
        )

print("")

for row in data:
    #print(row["description"].replace("'", "\\'"))
    try:
        print(
            "INSERT INTO Events(title, descr, category, dtime, cphone, "
            "cemail, urestriction, approved, lid) "
            "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', "
            "(SELECT lid FROM Locations WHERE lname='{}'"
            "));".format(
                row["title"].replace("'", "''"), row["description"].replace("'", "''"), row["category"],
                row["dtime"], row["contact_phone"].replace(".", "").replace("-", ""), row["contact_email"],
                1, 1, row["location"]))
    except:
        pass
