import pickle
import sys
from bs4 import BeautifulSoup

#python colorize_svg [flu_counts]

flu = pickle.load(open(sys.argv[1]))

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

# Output map
#print soup.prettify()


# Color the counties based on unemployment rate
for p in paths:

    if p['id'] in flu:
        # pass
        try:
            rate = flu[p['id']]
        except:
            continue
 
        if rate > 500:
            color_class = 4
        elif rate > 250:
            color_class = 3
        elif rate > 100:
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
print soup.prettify()
