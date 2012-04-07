import sys
import fileinput
import operator
import pickle
import time

#python user_list.py location_data.in out/user_checkins.out out/austin.out

users = {}
austin = {}
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

    columbus = sanfo = jacksonville = indianapolis = 0

    #find Austin-ers
    for u in users:
        checkins = users[u]
        austin_count = 0
        coh = sfo = jfl = iin = 0
        for city,date in checkins:
            if city == "Austin,TX":
                austin_count += 1
            if city == "Columbus,OH":
                coh += 1
            if city == "San Francisco,CA":
                sfo += 1
            if city == "Jacksonville,FL":
                jfl += 1
            if city == "Indianapolis,IN":
                iin += 1
        a_percent = austin_count/float(len(checkins))
        if a_percent >= .5:
            austin[u] = checkins
        c_percent = coh/float(len(checkins))
        if c_percent >= .5:
            columbus += 1
        s_percent = sfo/float(len(checkins))
        if s_percent >= .5:
            sanfo += 1
        j_percent = jfl/float(len(checkins))
        if j_percent >= .5:
            jacksonville += 1
        i_percent = iin/float(len(checkins))
        if i_percent >= .5:
            indianapolis += 1

    print "Austin: " + str(len(austin))
    print "Columbus: " + str(columbus)
    print "San Francisco: " + str(sanfo)
    print "Jacksonville: " + str(jacksonville)
    print "Indianapolis: " + str(indianapolis)

    #remove Austin-ers from original user list
    for u in austin:
        del users[u]


    checkin_list = open(sys.argv[2], 'w')

    for user in users:
        out = user
        checkins = users[user]
        for loc,date in checkins:
            out += "|" + loc + ">" + time.strftime(fmt, date)
        checkin_list.write(out + "\n")

    checkin_list.close()

    austin_list = open(sys.argv[3], 'w')

    for user in austin:
        out = user
        checkins = austin[user]
        for loc,date in checkins:
            out += "|" + loc + ">" + time.strftime(fmt, date)
        austin_list.write(out + "\n")

    austin_list.close()


#    pickle.dump(users, open("out/users.p", "wb"))

