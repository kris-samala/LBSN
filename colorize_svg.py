import pickle
import sys
import fileinput
import csv
from bs4 import BeautifulSoup

#python colorize_svg [maps] states.p [out]

# Load the SVG map
svg = open('../maps/Blank_US.svg', 'r').read()

# Load into Beautiful Soup
soup = BeautifulSoup(svg)

# Find states
paths = soup.findAll('path')

# Map colors
colors = ["#FECCCC", "#FF6565", "#FF0000", "#990000", "#320000"]

    # State style
path_style="fill-opacity:1;stroke:#ffffff;stroke-opacity:1;stroke-width:0.75;stroke-miterlimit:4;stroke-dasharray:none"

reader = csv.reader(open(sys.argv[1], 'rb'), delimiter=',')
transpose = zip(*reader)
states = pickle.load(open(sys.argv[2], 'rb'))

count=0
#for l in fileinput.input(sys.argv[1]):
#    flu = {}
#    line = l.split(",")
#    for pair in line:
#        if len(pair) > 1:
#            p = pair.split(":")
#            flu[p[0]] = float(p[1])

for k in range(0,52):
    flu = {}
    for i in range(1, 50):
        flu[states[i-1]] = float(list(transpose[i])[k])


    # Color the states based on flu incidences
    for p in paths:
        if p['id'] in flu:
            # pass
            try:
                rate = flu[p['id']]
                print rate
            except:
                continue

            if rate > .05:
                color_class = 4
            elif rate > .03:
                color_class = 3
            elif rate > .01:
                color_class = 2
            elif rate > .005:
                color_class = 1
            else:
                color_class = 0

            color = colors[color_class]
            p['style'] = "fill:" + color + ";" + path_style
        else:
            p['style'] = "fill:#d3d3d3;" + path_style

    # Output map
    out = open(sys.argv[3]+str(count)+".svg", "wb")
    out.write(soup.prettify())

    count+=1
