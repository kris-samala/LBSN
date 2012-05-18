#!/bin/bash

for i in `seq 1 52`;
do
  python colorize_svg.py full_maps/flu$i > full_maps/testmap$i.svg
done
