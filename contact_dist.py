import sys
import fileinput
import operator
import pickle
from datetime import datetime

#python contact_dist.py location_data.in out/contact_dist.out

fmt = "%Y-%m-%d"
days = {}
contacts = []
out = open(sys.argv[2], 'wb')

if len(sys.argv) < 2:
    print "Filename required"
else:
    for line in fileinput.input(sys.argv[1]):
        l = line.split("\t")
        date = datetime.strptime(l[8].split()[0], fmt)
        if date not in days:
            days[date] = []
        lines = days[date]
        lines.append(line)

    for d in days:
        cities = {}
        for line in days[d]:
            l = line.split("\t")
            city = l[2].rstrip()
            state = l[3].lstrip()
            city_state = city + "," + state
            userID = l[7].rstrip()
            if city_state not in cities:
                cities[city_state] = set()
            users = cities[city_state]
            users.add(userID)
        for c in cities:
            u = cities[c]
            contacts.append(len(u))

    for c in contacts:
        out.write(str(c) + ",")

out.close()
