import sys
import fileinput
import pickle
import math
import operator

#python fix_locations.py location_data_raw.in census.p city_coordinates.p location_data.in

census = pickle.load(open(sys.argv[2], 'rb'))
city_coords = pickle.load(open(sys.argv[3], 'rb'))
found = {}
R = 3961

def find_city(x, y):
    closest = []
    for c in census:
        if c in city_coords:
            x2, y2 = city_coords[c]
            y2 = -y2
            d = distance(x, y, x2, y2)
            if d < 150.0:
                closest.append((c ,d))

    sorted_closest = sorted(closest, key=operator.itemgetter(1))

    if len(sorted_closest) > 1:
        city, dist = sorted_closest[0]
        return city
    else:
        return None


def convert(x1, y1, x2, y2):
    x1 = math.radians(x1)
    y1 = math.radians(y1)
    x2 = math.radians(x2)
    y2 = math.radians(y2)

    return x1, y1, x2, y2


def distance(x1, y1, x2, y2):
    lat1, lon1, lat2, lon2 = convert(x1, y1, x2, y2)
    dlat = lat2-lat1
    dlon = lon2-lon1

    a = math.pow(math.sin(dlat/2.0),2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon/2.0),2)
    c = 2.0 * math.atan2( math.sqrt(a), math.sqrt(1.0-a) )
    d = R * c

    return d

out = open(sys.argv[4], 'wb')

err = open('not_found.out', 'wb')

if len(sys.argv) < 4:
    print "Filename required."
else:
    count = 0
    for l in fileinput.input(sys.argv[1]):
        line = l.split('\t')
        location = line[2].rstrip() + "," + line[3].lstrip()
        longitude = float(line[4])
        latitude = float(line[5])
        if location not in census:
            new_loc = find_city(latitude, longitude)
            if new_loc is not None:
                new_loc = new_loc.split(',')
                new_loc = "\t".join(new_loc)
                pre = "\t".join(line[0:2])
                post = "\t".join(line[4:])
                new_line = pre + '\t' + new_loc + '\t' + post
                out.write(new_line)
            else:
                err.write(location + ' ' + str(latitude) + ' ' + str(longitude) +'\n')
        else:
            out.write(l)

out.close()
err.close()
