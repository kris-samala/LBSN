#!/bin/bash

for i in `seq 1 52`;
do
  python colorize_svg.py maps/flu$i > maps/testmap$i.svg
done
