import sys
import fileinput
import pickle

#python parse_census.py [state_abbr] [census_raw] census.out

out = open(sys.argv[3], 'wb')
census = {}
state_abb = {}

if len(sys.argv) < 4:
    print "Filename required."
else:
    for line in fileinput.input(sys.argv[1]):
        line = line.split(',')
        state_abb[line[0]] = line[1]

    for line in fileinput.input(sys.argv[2]):
        line = line.split(',')
        city = line[2].lstrip('"')
        city = city.replace('city','').replace('village','').replace('CDP','').replace('town','').replace('municipality','').replace('zona urbana','').rstrip()
        state = line[3].lstrip().rstrip('"')
        state = state_abb[state].rstrip()
        pop = line[4]
        loc = city + "," + state
        census[loc] = int(pop)

    for l in census:
        out.write(l + " = " + str(census[l]) + "\n")

out.close()

pickle.dump(census, open('census.p', 'wb'))
