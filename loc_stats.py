import sys
import fileinput
import operator
import pickle

#python loc_stats.py location_data.in out/location_stats.out

locations = {}
coords = {}
cities = {}
states = {}

if len(sys.argv) < 2:
    print "Filename required."
else:
    #read location_data
    for line in fileinput.input(sys.argv[1]):
        line = line.split("\t")
        city = line[2].rstrip()
        state = line[3].lstrip()
        city_state = city + "," + state

        longitude = float(line[4])
        latitude = float(line[5])
        latd = longd = 0.0
        if city_state in coords:
            latd, longd = coords[city_state]
        latd += latitude
        longd += longitude
        coords[city_state] = (latd,longd)

        userID = line[7].rstrip()
        users = set()
        if city_state in locations:
            users = locations[city_state]
        users.add(userID)
        locations[city_state] = users

        if city_state not in cities:
            cities[city_state] = 1
        else:
            cities[city_state] += 1

        if state not in states:
            states[state] = 1
        else:
            states[state] += 1

    pickle.dump(locations, open("out/locations.p", "wb"))

    for city in coords:
        count = cities[city]
        latd, longd = coords[city]
        latd /= count
        longd /= count
        coords[city] = (latd,longd)
    pickle.dump(coords, open("out/coordinates.p", "wb"))


    sorted_cities = sorted(cities.iteritems(), key=operator.itemgetter(1), reverse = True)
    sorted_states = sorted(states.iteritems(), key=operator.itemgetter(1), reverse = True)

    loc_stats = open(sys.argv[2], 'w')
    loc_stats.write("#Total Cities: " + str(len(cities)) + "\n")

    for (city, count) in sorted_cities:
        loc_stats.write(city + " : " + str(count) + "\n")


    loc_stats.write("\n#Total States: " + str(len(states)) + "\n")
    for (state, count) in sorted_states:
        loc_stats.write(state + " : " + str(states[state]) + "\n")

    loc_stats.close()
