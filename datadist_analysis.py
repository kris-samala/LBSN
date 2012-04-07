import sys
import fileinput
import operator
import pickle
from datetime import datetime
import math

#python datadist_analysis.py location_data.in data_info.out
#extracts time and distance differences between checkins for each user history
#outputs frequent/problem users, data distribution analysis for charting
#assumes bad checkins are >600mph

users = {}
fmt = "%Y-%m-%d %H:%M:%S"
yrmo = "%Y-%m"
year09 = {}
year10 = {}
frequent = {}
R = 3961

def convert(x1, y1, x2, y2):
    x1 = math.radians(x1)
    y1 = math.radians(y1)
    x2 = math.radians(x2)
    y2 = math.radians(y2)

    return x1, y1, x2, y2

def d(x1, y1, x2, y2):
    lat1, lon1, lat2, lon2 = convert(x1, y1, x2, y2)
    dlat = lat2-lat1
    dlon = lon2-lon1

    a = math.pow(math.sin(dlat/2.0),2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon/2.0),2)
    c = 2.0 * math.atan2( math.sqrt(a), math.sqrt(1.0-a) )
    d = R * c

    return d


def distance(a, b):
    x1, y1 = a
    x2, y2 = b

    return d(x1, y1, x2, y2)

def time(a, b):
    timedelta = b - a
    days = timedelta.days
    fraction = timedelta.seconds / 86400.0
    return days+fraction


if len(sys.argv) < 2:
    print "Filename required."
else:
    for line in fileinput.input(sys.argv[1]):
        line = line.split("\t")
        location = line[2].rstrip() + "," + line[3].lstrip()
        latitude = float(line[5])
        longitude = float(line[4])
        userID = line[7].rstrip()
        date = datetime.strptime(line[8].rstrip(), fmt)
        if (date.year == 2010):
            if date.month in year10:
                year10[date.month] += 1
            else:
                year10[date.month] = 1

        if (date.year == 2009):
            if date.month in year09:
                year09[date.month] += 1
            else:
                year09[date.month] = 1

        checkins = []
        if userID in users:
            checkins = users[userID]

        checkins.append(((latitude, longitude), date))
        users[userID] = checkins

    for u in users:
        checkins = users[u]
        sorted_checkins = sorted(checkins, key=operator.itemgetter(1))
        users[u] = sorted_checkins


    checkin_list = open(sys.argv[2], 'w')

    mindate = maxdate = None
    for user in users:
        out = str(len(users[user]))
        checkins = users[user]
        first = prevloc = prevdate = None
        for loc,date in checkins:
            if prevloc is not None and prevdate is not None:
                dist = distance(prevloc, loc)
                time_d = time(prevdate, date)
                speed = 0
                if time_d > 0:
                    speed = dist / (time_d * 24)
                else:
                    speed = dist / (.00001 * 24)
                if speed > 600:
                    if user not in frequent:
                        frequent[user] = []
                    times = frequent[user]
                    times.append(prevdate)
                    times.append(date)
                    frequent[user] = times
                out += " " + str(dist) + "," + str(time_d)
            else:
                first = date
            prevloc = loc
            prevdate = date
        out += " " + str(time(first, prevdate))
        checkin_list.write(out + "\n")
        if mindate is None or first < mindate:
            mindate = first
        if maxdate is None or prevdate > maxdate:
            maxdate = prevdate

    checkin_list.close()

    pickle.dump(year09, open('out/year09.p', 'wb'))
    pickle.dump(year10, open('out/year10.p', 'wb'))


    freq = open("out/freq.out", 'wb')
    for user in frequent:
        out = user
        for t in frequent[user]:
            out += " " + str(t)
        freq.write(out + "\n")
    freq.close()

