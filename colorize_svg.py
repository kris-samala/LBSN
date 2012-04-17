import pickle
import sys
import fileinput
from bs4 import BeautifulSoup

#python colorize_svg [maps] [out]

# Load the SVG map
svg = open('maps/Blank_US.svg', 'r').read()

# Load into Beautiful Soup
soup = BeautifulSoup(svg)

# Find states
paths = soup.findAll('path')

# Map colors
colors = ["#FECCCC", "#FF6565", "#FF0000", "#990000", "#320000"]

    # State style
path_style="fill-opacity:1;stroke:#ffffff;stroke-opacity:1;stroke-width:0.75;stroke-miterlimit:4;stroke-dasharray:none"


count=0
for l in fileinput.input(sys.argv[1]):
    flu = {}
    line = l.split(",")
    for pair in line:
        if len(pair) > 1:
            p = pair.split(":")
            flu[p[0]] = int(p[1])

    # Color the states based on flu incidences
    for p in paths:
        if p['id'] in flu:
            # pass
            try:
                rate = flu[p['id']]
            except:
                continue

            if rate > 5000:
                color_class = 4
            elif rate > 2500:
                color_class = 3
            elif rate > 500:
                color_class = 2
            elif rate > 50:
                color_class = 1
            else:
                color_class = 0

            color = colors[color_class]
            p['style'] = "fill:" + color + ";" + path_style
        else:
            p['style'] = "fill:#d3d3d3;" + path_style

    # Output map
    out = open(sys.argv[2]+str(count)+".svg", "wb")
    out.write(soup.prettify())

    count+=1
