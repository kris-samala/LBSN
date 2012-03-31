import sys
import fileinput
import pickle

#python parse_citycoor.py city_coor.csv city_coor.out

out = open(sys.argv[2], "wb")
coords = {}

if len(sys.argv) < 2:
    print "Filename required."
else:
    for line in fileinput.input(sys.argv[1]):
        if line.startswith('['):
            line = line.split(None, 3)
            loc = line[3].rstrip()
            lat = float(line[1])
            longd = float(line[2])
            coords[loc] = (lat, longd)

    for c in coords:
        out.write(c + " " + str(coords[c]) + "\n")

out.close()

pickle.dump(coords, open('city_coordinates.p', 'wb'))
