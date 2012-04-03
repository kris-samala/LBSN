import sys
import fileinput
import operator
import pickle
import time

#python user_list.py location_data.in out/user_checkins.out

users = {}
fmt = "%Y-%m-%d %H:%M:%S"

if len(sys.argv) < 2:
    print "Filename required."
else:
    for line in fileinput.input(sys.argv[1]):
        line = line.split("\t")
        location = line[2].rstrip() + "," + line[3].lstrip()
        userID = line[7].rstrip()
        date = time.strptime(line[8].rstrip(), fmt)
        checkins = []
        if userID in users:
            checkins = users[userID]

        checkins.append((location, date))
        users[userID] = checkins

    for u in users:
        checkins = users[u]
        sorted_checkins = sorted(checkins, key=operator.itemgetter(1))
        users[u] = sorted_checkins


    checkin_list = open(sys.argv[2], 'w')

    for user in users:
        out = user
        checkins = users[user]
        for loc,date in checkins:
            out += "|" + loc + ">" + time.strftime(fmt, date)
        checkin_list.write(out + "\n")

    checkin_list.close()

#    pickle.dump(users, open("out/users.p", "wb"))

